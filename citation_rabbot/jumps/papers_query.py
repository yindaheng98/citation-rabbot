from argparse import ArgumentParser
from typing import Tuple, Dict, List
from .papers_args import add_arguments_papers, parse_args_papers


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
