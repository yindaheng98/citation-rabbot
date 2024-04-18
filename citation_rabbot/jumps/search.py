from citation_rabbot.rabbot import Jump
from typing import Tuple, Dict, List
from .papers_display import papers_results2message
from .papers_args import add_arguments_papers, parse_args_papers


def search_by_title_args2querys(args: object) -> List[Tuple[str, Dict]]:
    pwhere, jwhere, orderby, limits, values = parse_args_papers(args)
    return [(
        f"MATCH (p:Publication) WHERE {pwhere} " +
        ("OPTIONAL MATCH (p:Publication)-[:PUBLISH]->(j:Journal) " if jwhere == '' else f"MATCH (p:Publication)-[:PUBLISH]->(j:Journal) WHERE {jwhere} ") +
        f"OPTIONAL MATCH (c:Publication)-[:CITE]->(p:Publication) "
        f"OPTIONAL MATCH (r:Publication)<-[:CITE]-(p:Publication) "
        f"RETURN p, j, COUNT(DISTINCT c) AS citation, COUNT(DISTINCT r) AS reference ORDER BY {orderby} LIMIT {limits}",
        values
    )]


search_by_title_jump = Jump(
    name="search_by_title",
    parser_add_arguments=add_arguments_papers,
    args2querys=search_by_title_args2querys,
    results2message=papers_results2message,
    description="Search papers by keywords in title"
)
