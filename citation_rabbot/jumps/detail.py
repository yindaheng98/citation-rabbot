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
    return [(
        f"MATCH (p:Publication) WHERE p.{paper_k}=$value "
        f"MATCH (c:Publication)-[:CITE]->(p:Publication)-[:CITE]->(r:Publication) "
        f"MATCH (a:Person)-[:WRITE]->(p:Publication)-[:PUBLISH]->(j:Journal) "
        "RETURN a, p, j, count(c), count(r) AS citation ORDER BY citation DESC",
        {"value": paper_v}
    )]


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
    authors = []
    papers = []
    for author, paper, journal, cited, refed in res[0]:
        author_msg = f'{author["name"]}'
        if "dblp_id" in author:
            author_msg = f'<a href="https://doi.org/pid/{author["dblp_id"]}.html">{author["name"]}</a>'
        authors.append(author_msg)

        title = paper['title']
        info = f"{journal['dblp_name']} (CCF {journal['ccf']}), {paper['date'] if 'date' in paper else paper['year']}"
        paper_msg = f"{title}, {info}, {refed} references, {cited} citations\n"
        if "doi" in paper:
            paper_msg = f'<a href="https://doi.org/{paper["doi"]}">{title}</a>, {info}, {refed} references, {cited} citations\n'
        if paper_msg not in papers:
            papers.append(paper_msg)

    msg = "\n".join(papers) + "\n<b>Authors: </b>" +", ".join(authors)
    return msg, InlineKeyboardMarkup(keyboards)


paper_detail_jump = (
    "paper_detail",
    paper_detail_parser_add_arguments,
    paper_detail_args2querys,
    papers_detail_results2message,
    None
)
