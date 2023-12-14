from argparse import ArgumentParser
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from typing import Tuple, Dict, List

authors_parser = ArgumentParser()
authors_parser.add_argument('key', metavar='key', type=str,
                            help='Key and value to identify the paper')
authors_parser.add_argument('value', metavar='value', type=str,
                            help='Key and value to identify the paper')


def paper_authors_args2querys(args: object) -> List[Tuple[str, Dict]]:
    papers_k, author_v = args.key, args.value
    return [(
        f"MATCH (a:Person)-[:WRITE]->(p:Publication) WHERE p.{papers_k}=$value "
        "MATCH (a:Person)-[:WRITE]->(c:Publication) "
        "RETURN a, count(c) AS citation ORDER BY citation DESC",
        {"value": author_v}
    )]


def authors_results2message(res: List, args: object):
    msg = ""
    keyboard = []
    for i, (node, papers) in enumerate(res[0]):
        name = node['name']
        msg += f"{i+1}. {papers} papers: {name}\n"
        k, v = None, None
        if "dblp_id" in node:
            k, v = "dblp_id", node["dblp_id"]
        elif "authorId" in node:
            k, v = "authorId", node["authorId"]
        if k is not None:
            keyboard.append([
                InlineKeyboardButton(f"{i+1}'s Papers", switch_inline_query_current_chat=f"/author_papers {k}:{v}"),
            ])
    if msg == "":
        msg = "No authors yet"
    return msg, InlineKeyboardMarkup(keyboard)


paper_authors_jump = ("paper_authors", authors_parser, paper_authors_args2querys, authors_results2message, None)