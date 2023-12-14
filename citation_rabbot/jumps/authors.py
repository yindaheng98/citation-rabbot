from argparse import ArgumentParser
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from typing import Tuple, Dict, List
from .papers_args import add_arguments_papers
from .papers_display import reconstruct_paper_args


def authors_parser_add_arguments(authors_parser):
    authors_parser.add_argument('key', metavar='key', type=str,
                                help='Key and value to identify the paper')
    authors_parser.add_argument('value', metavar='value', type=str,
                                help='Key and value to identify the paper')
    return add_arguments_papers(authors_parser)


def paper_authors_args2querys(args: object) -> List[Tuple[str, Dict]]:
    paper_k, paper_v = args.key, args.value
    return [(
        f"MATCH (a:Person)-[:WRITE]->(p:Publication) WHERE p.{paper_k}=$value "
        "MATCH (a:Person)-[:WRITE]->(c:Publication) "
        "RETURN a, count(c) AS citation ORDER BY citation DESC",
        {"value": paper_v}
    )]


def authors_results2message(res: List, args: object):
    msg = ""
    paper_args = reconstruct_paper_args(args)
    keyboards = []
    for i, (node, papers) in enumerate(res[0]):
        name = node['name']
        msg += f"{i+1}. {papers} papers: {name}\n"
        k, v = None, None
        if "dblp_id" in node:
            k, v = "dblp_id", node["dblp_id"]
        elif "authorId" in node:
            k, v = "authorId", node["authorId"]
        if k is not None:
            keyboards.append(
                InlineKeyboardButton(
                    f"{i+1}'s Papers",
                    switch_inline_query_current_chat=f"/author_papers {paper_args} {k} {v}"
                )
            )
    if msg == "":
        msg = "No authors yet"
    N = 3
    keyboard = []
    for i in range(len(keyboards) // N + 1):
        keyboard.append([])
        for j in range(N):
            if i*3+j < len(keyboards):
                keyboard[-1].append(keyboards[i*3+j])
    return msg, InlineKeyboardMarkup(keyboard)


paper_authors_jump = (
    "paper_authors",
    authors_parser_add_arguments,
    paper_authors_args2querys,
    authors_results2message,
    None
)
