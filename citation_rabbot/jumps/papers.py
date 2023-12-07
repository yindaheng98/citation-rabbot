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
                InlineKeyboardButton(f"{i+1}'s Papers", switch_inline_query_current_chat=f"/author_papers title_hash:{node['title_hash']}"),
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
        "MATCH (c:Publication)-[:CITE]->(p:Publication) "
        "RETURN p, COUNT(c) AS ct ORDER BY ct DESC" % paper_k,
        {"value": paper_v}
    )]


def papers_results2message(res: List):
    msg = ""
    keyboard = []
    for i, (node, cited) in enumerate(res[0]):
        title = node['title']
        msg += f"{i+1}: {cited} cited: {title} {node['year']}\n"
        keyboard.append([
            InlineKeyboardButton(f"{i+1}'s Authors", switch_inline_query_current_chat=f"/paper_authors title_hash:{node['title_hash']}"),
            InlineKeyboardButton(f"{i+1}'s Citations", switch_inline_query_current_chat=f"/citations title_hash:{node['title_hash']}"),
            InlineKeyboardButton(f"{i+1}'s References", switch_inline_query_current_chat=f"/references title_hash:{node['title_hash']}"),
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
        "MATCH (c:Publication)-[:CITE]->(a:Publication) "
        "RETURN a, count(c) AS ct ORDER BY ct DESC" % paper_k,
        {"value": paper_v}
    )]


def citations_message2querys(msg: str) -> List[Tuple[str, Dict]]:
    splited = re.findall(r"^/[A-Za-z_]+ +([A-Za-z_]+):(\S+)$", msg)
    if len(splited) <= 0:
        return
    paper_k, paper_v = splited[0]
    return [(
        "MATCH (a:Publication)-[:CITE]->(:Publication {%s:$value}) "
        "MATCH (c:Publication)-[:CITE]->(a:Publication) "
        "RETURN a, count(c) AS ct ORDER BY ct DESC" % paper_k,
        {"value": paper_v}
    )]


paper_authors_jump = ("paper_authors", paper_authors_message2querys, authors_results2message)
author_papers_jump = ("author_papers", author_papers_message2querys, papers_results2message)
references_jump = ("references", references_message2querys, papers_results2message)
citations_jump = ("citations", citations_message2querys, papers_results2message)
