from telegram import Message
from typing import Tuple, Dict, List
import re


def paper_authors_message2querys(msg: Message) -> List[Tuple[str, Dict]]:
    splited = re.findall(r"^/[A-Za-z_]+ +([A-Za-z_]+):(\s+)$", msg.text)
    if len(splited) < 2:
        return
    paper_k, paper_v = splited
    return [(
        "MATCH (a:Person)-[:WRITE]->(p:Publication {%s:$value}) "
        "MATCH (a:Person)-[:WRITE]->(c:Publication) "
        "RETURN a, count(c) AS ct ORDER BY ct DESC" % paper_k,
        {"value": paper_v}
    )]


def authors_results2message(res: List) -> str:
    pass


def author_papers_message2querys(msg: Message) -> List[Tuple[str, Dict]]:
    splited = re.findall(r"^/[A-Za-z_]+ +([A-Za-z_]+):(\S+)$", msg.text)
    if len(splited) <= 0:
        return
    paper_k, paper_v = splited[0]
    return [(
        "MATCH (a:Person {%s:$value})-[:WRITE]->(p:Publication) "
        "MATCH (c:Publication)-[:CITE]->(p:Publication) "
        "RETURN p, COUNT(c) AS ct ORDER BY ct DESC" % paper_k,
        {"value": paper_v}
    )]


def papers_results2message(res: List) -> str:
    msg = ""
    for node, cited in res[0]:
        title = node['title']
        msg += f"{cited} cited: {title}\n"
    return msg


def references_message2querys(msg: Message) -> List[Tuple[str, Dict]]:
    pass


def citations_message2querys(msg: Message) -> List[Tuple[str, Dict]]:
    pass


paper_authors_jump = ("paper_authors", paper_authors_message2querys, authors_results2message)
author_papers_jump = ("author_papers", author_papers_message2querys, papers_results2message)
references_jump = ("references", references_message2querys, papers_results2message)
citations_jump = ("citations", citations_message2querys, papers_results2message)
