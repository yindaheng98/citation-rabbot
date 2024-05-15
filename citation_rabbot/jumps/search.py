from citation_rabbot.models import Jump
from typing import Tuple, Dict, List
from .papers_display import papers_results2message
from .papers_args import add_arguments_papers, parse_args_papers, parse_args_papers_fulltext_index


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


def search_by_title_semantic_args2querys(args: object) -> List[Tuple[str, Dict]]:
    lucene, pwhere, jwhere, orderby, limits, values = parse_args_papers_fulltext_index(args)
    return [(
        f"CALL db.index.fulltext.queryNodes('publication_title_fulltext_index', '{lucene}') YIELD node WHERE {pwhere} WITH node AS p " +
        ("OPTIONAL MATCH (p:Publication)-[:PUBLISH]->(j:Journal) " if jwhere == '' else f"MATCH (p:Publication)-[:PUBLISH]->(j:Journal) WHERE {jwhere} ") +
        f"OPTIONAL MATCH (c:Publication)-[:CITE]->(p:Publication) "
        f"OPTIONAL MATCH (r:Publication)<-[:CITE]-(p:Publication) "
        f"RETURN p, j, COUNT(DISTINCT c) AS citation, COUNT(DISTINCT r) AS reference ORDER BY {orderby} LIMIT {limits}",
        values
    )]


search_by_title_semantic_jump = Jump(
    name="search_by_title_semantic",
    parser_add_arguments=add_arguments_papers,
    args2querys=search_by_title_semantic_args2querys,
    results2message=papers_results2message,
    description="Search papers by keywords in title semantically"
)


def search_by_abstract_semantic_args2querys(args: object) -> List[Tuple[str, Dict]]:
    lucene, pwhere, jwhere, orderby, limits, values = parse_args_papers_fulltext_index(args)
    return [(
        f"CALL db.index.fulltext.queryNodes('publication_abstract_fulltext_index', '{lucene}') YIELD node WITH node AS p " +
        f"MATCH (p:Publication) WHERE {pwhere} " +
        ("OPTIONAL MATCH (p:Publication)-[:PUBLISH]->(j:Journal) " if jwhere == '' else f"MATCH (p:Publication)-[:PUBLISH]->(j:Journal) WHERE {jwhere} ") +
        f"OPTIONAL MATCH (c:Publication)-[:CITE]->(p:Publication) "
        f"OPTIONAL MATCH (r:Publication)<-[:CITE]-(p:Publication) "
        f"RETURN p, j, COUNT(DISTINCT c) AS citation, COUNT(DISTINCT r) AS reference ORDER BY {orderby} LIMIT {limits}",
        values
    )]


search_by_abstract_semantic_jump = Jump(
    name="search_by_abstract_semantic",
    parser_add_arguments=add_arguments_papers,
    args2querys=search_by_abstract_semantic_args2querys,
    results2message=papers_results2message,
    description="Search papers by keywords in abstract semantically"
)
