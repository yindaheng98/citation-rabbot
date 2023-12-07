from typing import Tuple, Dict, List
import re
from .papers import papers_results2message

limit = 20

def search_by_title_message2querys(msg: str) -> List[Tuple[str, Dict]]:
    match = re.findall(r"^/[A-Za-z_]+ +([A-Za-z_ ]+)$", msg)
    if len(match) <= 0:
        return
    split = [s for s in match[0].split(" ") if len(s) > 0]
    if len(split) <= 0:
        return
    init_match = "MATCH (p:Publication) WHERE toLower(p.title) CONTAINS $value0 "
    values = {"value0": split[0].lower()}
    for i, s in enumerate(split[1:]):
        init_match += f"toLower(p.title) CONTAINS $value{i+1} "
        values[f"$value{i+1}"] = s.lower()
    return [(
        init_match +
        "MATCH (c:Publication)-[:CITE]->(p:Publication)-[:PUBLISH]->(j:Journal) "
        f"RETURN p, j, COUNT(c) AS ct ORDER BY ct DESC LIMIT {limit}",
        values
    )]


search_by_title_jump = ("search_by_title", search_by_title_message2querys, papers_results2message, "Search papers by keywords in title")
