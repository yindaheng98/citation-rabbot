from typing import Tuple, Dict, List
from .papers import papers_results2message
from .args import parser, parse_args_papers


def search_by_title_args2querys(args: object) -> List[Tuple[str, Dict]]:
    where, orderby, limits, values = parse_args_papers(args)
    return [(
        f"MATCH (c:Publication)-[:CITE]->(p:Publication)-[:PUBLISH]->(j:Journal) WHERE {where} "
        f"RETURN p, j, COUNT(c) AS citation ORDER BY {orderby} LIMIT {limits}",
        values
    )]


search_by_title_jump = ("search_by_title", parser, search_by_title_args2querys,
                        papers_results2message, "Search papers by keywords in title")
