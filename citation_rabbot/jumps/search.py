from argparse import ArgumentParser
from typing import Tuple, Dict, List
from .papers_display import papers_results2message
from .papers_args import add_arguments_papers, parse_args_papers


def search_by_title_args2querys(args: object) -> List[Tuple[str, Dict]]:
    where, orderby, limits, values = parse_args_papers(args)
    return [(
        f"MATCH (c:Publication)-[:CITE]->(p:Publication)-[:PUBLISH]->(j:Journal) WHERE {where} "
        f"RETURN p, j, COUNT(c) AS citation ORDER BY {orderby} LIMIT {limits}",
        values
    )]


search_by_title_jump = (
    "search_by_title",
    add_arguments_papers(ArgumentParser()),
    search_by_title_args2querys,
    papers_results2message,
    "Search papers by keywords in title"
)
