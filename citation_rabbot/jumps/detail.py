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
            f"References",
            switch_inline_query_current_chat=f'/references {paper_args} "{paper_k}" "{paper_v}"'),
        InlineKeyboardButton(
            f"Citations",
            switch_inline_query_current_chat=f'/citations {paper_args} "{paper_k}" "{paper_v}"'),
    ]]

    papers, journals, citations, references, authors = res

    author_details, author_keyboards = [], []
    for author, n_papers in authors:
        author_msg = f'{author["name"]}'
        k, v = None, None
        if "authorId" in author:
            k, v = "authorId", author["authorId"]
            author_msg = f'<a href="https://www.semanticscholar.org/author/{author["authorId"]}">{author["name"]}</a>'
        elif "dblp_pid" in author:
            k, v = "dblp_id", author["dblp_id"]
            author_msg = f'<a href="https://dblp.org/pid/{author["dblp_pid"]}.html">{author["name"]}</a>'
        author_details.append(f"{author_msg} {n_papers} papers")
        if k is not None:
            author_keyboards.append(
                InlineKeyboardButton(
                    f"{author['name']}",
                    switch_inline_query_current_chat=f'/author_papers {paper_args} "{k}" "{v}"'
                )
            )
    N = 3
    for i in range(len(author_keyboards) // N + 1):
        keyboards.append([])
        for j in range(N):
            if i*3+j < len(author_keyboards):
                keyboards[-1].append(author_keyboards[i*3+j])
    authors_msg = "\n<b>Authors: </b>\n " + "\n ".join(author_details)

    paper_msgs = []
    for (paper,), (journal,), (cited,), (refed,) in zip(papers, journals, citations, references):
        title = paper['title']
        info = f"<i>{journal['dblp_name']}</i> (CCF {journal['ccf']}), {paper['date'] if 'date' in paper else paper['year']}"
        paper_msg = f"{title}, {info}, {refed} references, {cited} citations\n"
        if "doi" in paper:
            paper_msg = f'<a href="https://doi.org/{paper["doi"]}">{title}</a>, {info}, {refed} references, {cited} citations\n'
        if paper_msg not in paper_msgs:
            paper_msgs.append(paper_msg)
    papers_msg = "\n".join(paper_msgs)
    msg = papers_msg + "\n" + authors_msg
    return msg, InlineKeyboardMarkup(keyboards)


paper_detail_jump = (
    "paper_detail",
    paper_detail_parser_add_arguments,
    paper_detail_args2querys,
    papers_detail_results2message,
    None
)