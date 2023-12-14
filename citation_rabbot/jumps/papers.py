from argparse import ArgumentParser
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from typing import Tuple, Dict, List
from .args import add_arguments_papers, parse_args_papers


def paper_authors_args2querys(args: object) -> List[Tuple[str, Dict]]:
    splited = []
    if len(splited) <= 0:
        return
    paper_k, paper_v = splited[0]
    return [(
        "MATCH (a:Person)-[:WRITE]->(p:Publication {%s:$value}) "
        "MATCH (a:Person)-[:WRITE]->(c:Publication) "
        "RETURN a, count(c) AS ct ORDER BY ct DESC" % paper_k,
        {"value": paper_v}
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


author_papers_parser = ArgumentParser()
author_papers_parser.add_argument('key', metavar='key', type=str,
                                  help='Key and value to identify the author')
author_papers_parser.add_argument('value', metavar='value', type=str,
                                  help='Key and value to identify the author')
author_papers_parser = add_arguments_papers(author_papers_parser)


def author_papers_args2querys(args: object) -> List[Tuple[str, Dict]]:
    where, orderby, limits, values = parse_args_papers(args)
    author_k, author_v = args.key, args.value
    return [(
        f"MATCH (a:Person)-[:WRITE]->(p:Publication) WHERE a.{author_k}=$value "
        f"MATCH (c:Publication)-[:CITE]->(p:Publication)-[:PUBLISH]->(j:Journal) WHERE {where} "
        f"RETURN p, j, COUNT(c) AS citation ORDER BY {orderby} LIMIT {limits}",
        {"value": author_v, **values}
    )]


def papers_results2message(res: List, args: object):
    msg = ""
    keyboard = []
    for i, (paper, journal, cited) in enumerate(res[0]):
        title = paper['title']
        info = f"{journal['dblp_name']} (CCF {journal['ccf']}),{paper['year']}"
        if "doi" in paper:
            msg += f'{i+1}: <b>{cited}</b> cited: <a href="https://doi.org/{paper["doi"]}">{title}</a>,{info}\n'
        else:
            msg += f"{i+1}: <b>{cited}</b> cited: {title},{info}\n"
        keyboard.append([
            InlineKeyboardButton(
                f"{i+1}'s Authors",
                switch_inline_query_current_chat=f"/paper_authors title_hash:{paper['title_hash']}"),
            InlineKeyboardButton(
                f"{i+1}'s Citations",
                switch_inline_query_current_chat=f"/citations title_hash:{paper['title_hash']}"),
            InlineKeyboardButton(
                f"{i+1}'s References",
                switch_inline_query_current_chat=f"/references title_hash:{paper['title_hash']}"),
        ])
    if msg == "":
        msg = "No papers yet"
    return msg, InlineKeyboardMarkup(keyboard)


papers_parser = ArgumentParser()
papers_parser.add_argument('key', metavar='key', type=str,
                           help='Key and value to identify the paper')
papers_parser.add_argument('value', metavar='value', type=str,
                           help='Key and value to identify the paper')
papers_parser = add_arguments_papers(papers_parser)


def references_args2querys(args: object) -> List[Tuple[str, Dict]]:
    where, orderby, limits, values = parse_args_papers(args)
    paper_k, paper_v = args.key, args.value
    return [(
        f"MATCH (p:Publication)<-[:CITE]-(a:Publication) WHERE a.{paper_k}=$value "
        f"MATCH (c:Publication)-[:CITE]->(p:Publication)-[:PUBLISH]->(j:Journal) WHERE {where} "
        f"RETURN p, j, COUNT(c) AS citation ORDER BY {orderby} LIMIT {limits}",
        {"value": paper_v, **values}
    )]


def citations_args2querys(args: object) -> List[Tuple[str, Dict]]:
    where, orderby, limits, values = parse_args_papers(args)
    paper_k, paper_v = args.key, args.value
    return [(
        f"MATCH (p:Publication)-[:CITE]->(a:Publication) WHERE a.{paper_k}=$value "
        f"MATCH (c:Publication)-[:CITE]->(p:Publication)-[:PUBLISH]->(j:Journal) WHERE {where} "
        f"RETURN p, j, COUNT(c) AS citation ORDER BY {orderby} LIMIT {limits}",
        {"value": paper_v, **values}
    )]


paper_authors_jump = ("paper_authors", paper_authors_args2querys, authors_results2message, None)
author_papers_jump = ("author_papers", author_papers_parser, author_papers_args2querys, papers_results2message, None)
references_jump = ("references", papers_parser, references_args2querys, papers_results2message, None)
citations_jump = ("citations", papers_parser, citations_args2querys, papers_results2message, None)
