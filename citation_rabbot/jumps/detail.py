from typing import Tuple, Dict, List
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from .papers_args import add_arguments_papers
from .papers_display import reconstruct_paper_args


def paper_detail_parser_add_arguments(detail_parser):
    detail_parser.add_argument('key', metavar='key', type=str,
                               help='Key and value to identify the paper')
    detail_parser.add_argument('value', metavar='value', type=str,
                               help='Key and value to identify the paper')
    return add_arguments_papers(detail_parser)


def paper_detail_args2querys(args: object) -> List[Tuple[str, Dict]]:
    paper_k, paper_v = args.key, args.value
    return [
        (f"MATCH (p:Publication) WHERE p.{paper_k}=$value RETURN p", {"value": paper_v}),
        (f"MATCH (p:Publication)-[:PUBLISH]->(j:Journal) WHERE p.{paper_k}=$value RETURN j", {"value": paper_v}),
        (f"MATCH (c:Publication)-[:CITE]->(p:Publication) WHERE p.{paper_k}=$value "
            "RETURN count(c) AS citation ORDER BY citation DESC", {"value": paper_v}),
        (f"MATCH (r:Publication)<-[:CITE]-(p:Publication) WHERE p.{paper_k}=$value "
            "RETURN count(r) AS citation ORDER BY citation DESC", {"value": paper_v}),
        (f"MATCH (a:Person)-[:WRITE]->(p:Publication) WHERE p.{paper_k}=$value "
            "MATCH (a:Person)-[:WRITE]->(c:Publication) "
            "RETURN a, count(c) AS citation ORDER BY citation DESC", {"value": paper_v}),
    ]


def papers_detail_results2message(res: List, args: object):
    msg = ""
    paper_args = reconstruct_paper_args(args)
    paper_k, paper_v = args.key, args.value
    keyboards = [[
        InlineKeyboardButton(
            f"Authors",
            switch_inline_query_current_chat=f'/paper_authors {paper_args} "{paper_k}" "{paper_v}"'),
        InlineKeyboardButton(
            f"References",
            switch_inline_query_current_chat=f'/references {paper_args} "{paper_k}" "{paper_v}"'),
        InlineKeyboardButton(
            f"Citations",
            switch_inline_query_current_chat=f'/citations {paper_args} "{paper_k}" "{paper_v}"'),
    ]]
    papers, journals, citations, references, authors = res
    author_msgs = []
    for author, n_papers in authors:
        author_msg = f'{author["name"]}'
        if "dblp_pid" in author:
            author_msg = f'<a href="https://dblp.org/pid/{author["dblp_pid"]}.html">{author["name"]}</a>'
        author_msgs.append(author_msg)
    paper_msgs = []
    for (paper,), (journal,), (cited,), (refed,) in zip(papers, journals, citations, references):
        title = paper['title']
        info = f"<i>{journal['dblp_name']}</i> (CCF {journal['ccf']}), {paper['date'] if 'date' in paper else paper['year']}"
        paper_msg = f"{title}, {info}, {refed} references, {cited} citations\n"
        if "doi" in paper:
            paper_msg = f'<a href="https://doi.org/{paper["doi"]}">{title}</a>, {info}, {refed} references, {cited} citations\n'
        if paper_msg not in paper_msgs:
            paper_msgs.append(paper_msg)

    msg = "\n".join(paper_msgs) + "\n<b>Authors: </b>" + ", ".join(author_msgs)
    return msg, InlineKeyboardMarkup(keyboards)


paper_detail_jump = (
    "paper_detail",
    paper_detail_parser_add_arguments,
    paper_detail_args2querys,
    papers_detail_results2message,
    None
)
