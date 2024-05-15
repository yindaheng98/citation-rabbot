from argparse import ArgumentParser
from enum import Enum
from datetime import datetime


class Order(Enum):
    Citation = 'citation'
    Year = 'year'
    Date = 'date'

    def __str__(self):
        return self.value


def add_arguments_papers_order(parser: ArgumentParser):
    parser.add_argument("-o", "--order", type=Order, choices=list(Order), default=Order.Citation,
                        help="Order by what.")
    return parser


def parse_args_papers_order(args: object):
    orderby = 'citation DESC'
    if args.order == Order.Year:
        orderby = 'p.year DESC, citation DESC'
    elif args.order == Order.Date:
        orderby = 'p.year DESC, COALESCE(p.date, date("1970-01-01")) DESC, citation DESC'
    return orderby


def add_arguments_papers_keyword(parser: ArgumentParser):
    parser.add_argument("-k", "--keyword", action='append', default=[],
                        help="Specify keyword rules for searching the title. "
                        "-k 'word1 word2' means 'word1 and word2', "
                        "-k 'word1' -k 'word2' means 'word1 or word2'. "
                        "e.g. -k 'video edge' -k 'super-resolution' means search for those papers "
                        "whose title includes both 'video' and 'edge' or includes 'super-resolution'")
    return parser


def parse_args_papers_keyword(args: object):
    pwhere, values = '', {}
    ki, k_or, v_or = 0, [], {}
    for keywords in args.keyword:
        k_and, v_and = [], {}
        for k in keywords.split(" "):
            if not k:
                continue
            ki += 1
            k_and.append(f"p.title_hash CONTAINS $keyword{ki}")
            v_and[f"keyword{ki}"] = k.lower()
        k_or.append(f"({' and '.join(k_and)})")
        v_or = {**v_or, **v_and}
    if ki > 0:
        pwhere += " AND " + f"({' OR '.join(k_or)})"
        values = {**values, **v_or}
    return pwhere, values


def parse_args_papers_keyword_lucene(args: object):
    k_or = []
    for keywords in args.keyword:
        k_and = []
        for k in keywords.split(" "):
            if not k:
                continue
            k_and.append(k.lower())
        k_or.append(f"{' '.join(k_and)}")
    if len(k_or) <= 0:
        return ''
    if 0 < len(k_or) <= 1:
        return k_or[0]
    return ' OR '.join([f'({k})' for k in k_or])


def add_arguments_papers_where(parser: ArgumentParser):
    parser.add_argument("-p", "--where_paper", action='append', default=[],
                        help="Specify rules for match paper in the database. "
                        "e.g. -p date>=date('2023-01-01') will only return those papers published after Jan 1, 2023")
    parser.add_argument("-j", "--where_journal", action='append', default=[],
                        help="Specify rules for match journal in the database. "
                        "e.g. -j ccf='A' will only return those CCF A papers")
    return parser


def parse_args_papers_where(args: object, perfix='p.'):
    pwhere = (
        " AND " + f"({' AND '.join([perfix + w for w in args.where_paper])})"
    ) if len(args.where_paper) > 0 else ""
    jwhere = ''
    if len(args.where_journal) > 0:
        jwhere = ' AND '.join(['j.' + w for w in args.where_journal])
    return pwhere, jwhere


def add_arguments_papers_base(parser: ArgumentParser):
    parser.add_argument("-y", "--year", type=int, default=datetime.now().year - 5,
                        help="Donot include those papers before this year.")
    parser.add_argument("-l", "--limit", type=int, help="Limit the length of results. Maximum 20", default=20)
    return parser


def parse_args_papers(args: object):
    orderby = parse_args_papers_order(args)

    limits = "$limit"
    pwhere = 'p.year >= $year'
    values = dict(year=args.year, limit=args.limit)

    kpwhere, kvalues = parse_args_papers_keyword(args)
    pwhere += kpwhere
    values = {**values, **kvalues}

    wpwhere, jwhere = parse_args_papers_where(args)
    pwhere += wpwhere
    return pwhere, jwhere, orderby, limits, values


def parse_args_papers_fulltext_index(args: object):
    orderby = parse_args_papers_order(args)

    limits = "$limit"
    pwhere = 'node.year >= $year'
    values = dict(year=args.year, limit=args.limit)

    lucenes = parse_args_papers_keyword_lucene(args)

    wpwhere, jwhere = parse_args_papers_where(args, perfix="node.")
    pwhere += wpwhere
    return lucenes, pwhere, jwhere, orderby, limits, values


def add_arguments_papers(parser: ArgumentParser):
    parser = add_arguments_papers_order(parser)
    parser = add_arguments_papers_keyword(parser)
    parser = add_arguments_papers_where(parser)
    parser = add_arguments_papers_base(parser)
    return parser
