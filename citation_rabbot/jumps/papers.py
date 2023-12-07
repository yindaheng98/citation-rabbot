from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from typing import Tuple, Dict, List
import re


def paper_authors_message2querys(msg: str) -> List[Tuple[str, Dict]]:
    splited = re.findall(r"^/[A-Za-z_]+ +([A-Za-z_]+):(\S+)$", msg)
    if len(splited) <= 0:
        return
    paper_k, paper_v = splited[0]
    return [(
        "MATCH (a:Person)-[:WRITE]->(p:Publication {%s:$value}) "
        "MATCH (a:Person)-[:WRITE]->(c:Publication) "
        "RETURN a, count(c) AS ct ORDER BY ct DESC" % paper_k,
        {"value": paper_v}
    )]


def authors_results2message(res: List):
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


def author_papers_message2querys(msg: str) -> List[Tuple[str, Dict]]:
    splited = re.findall(r"^/[A-Za-z_]+ +([A-Za-z_]+):(\S+)$", msg)
    if len(splited) <= 0:
        return
    paper_k, paper_v = splited[0]
    return [(
        "MATCH (a:Person {%s:$value})-[:WRITE]->(p:Publication) "
        "MATCH (c:Publication)-[:CITE]->(p:Publication)-[:PUBLISH]->(j:Journal) "
        "RETURN p, j, COUNT(c) AS ct ORDER BY ct DESC" % paper_k,
        {"value": paper_v}
    )]


def papers_results2message(res: List):
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


def references_message2querys(msg: str) -> List[Tuple[str, Dict]]:
    splited = re.findall(r"^/[A-Za-z_]+ +([A-Za-z_]+):(\S+)$", msg)
    if len(splited) <= 0:
        return
    paper_k, paper_v = splited[0]
    return [(
        "MATCH (a:Publication)<-[:CITE]-(:Publication {%s:$value}) "
        "MATCH (c:Publication)-[:CITE]->(a:Publication)-[:PUBLISH]->(j:Journal) "
        "RETURN a, j, count(c) AS ct ORDER BY ct DESC" % paper_k,
        {"value": paper_v}
    )]


def citations_message2querys(msg: str) -> List[Tuple[str, Dict]]:
    splited = re.findall(r"^/[A-Za-z_]+ +([A-Za-z_]+):(\S+)$", msg)
    if len(splited) <= 0:
        return
    paper_k, paper_v = splited[0]
    return [(
        "MATCH (a:Publication)-[:CITE]->(:Publication {%s:$value}) "
        "MATCH (c:Publication)-[:CITE]->(a:Publication)-[:PUBLISH]->(j:Journal) "
        "RETURN a, j, count(c) AS ct ORDER BY ct DESC" % paper_k,
        {"value": paper_v}
    )]


paper_authors_jump = ("paper_authors", paper_authors_message2querys, authors_results2message, None)
author_papers_jump = ("author_papers", author_papers_message2querys, papers_results2message, None)
references_jump = ("references", references_message2querys, papers_results2message, None)
citations_jump = ("citations", citations_message2querys, papers_results2message, None)
