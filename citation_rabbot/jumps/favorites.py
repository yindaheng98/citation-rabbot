import dbm
import os
import json
from telegram import InlineKeyboardButton
from citation_rabbot.models import Jump, Description
from .papers_args import add_arguments_papers, parse_args_papers
from .papers_display import papers_results2message

favorites_dirname = os.environ['RABBOT_FAVORITE_DIR'] if 'RABBOT_FAVORITE_DIR' in os.environ else "save/favorites"


def favorite_paper_parser_add_arguments(parser):
    parser.add_argument('key', metavar='key', type=str,
                        help='Key and value to identify the paper')
    parser.add_argument('value', metavar='value', type=str,
                        help='Key and value to identify the paper')
    return parser


def add_favorite_paper_args2querys(args: object):
    username = args.username
    favorites_paper_path = os.path.join(favorites_dirname, username, "papers")
    os.makedirs(os.path.dirname(favorites_paper_path), exist_ok=True)
    k, v = args.key, args.value.encode(encoding="utf8")
    with dbm.open(favorites_paper_path, 'c') as db:
        if v not in db:
            db[v] = json.dumps([k]).encode(encoding="utf8")
        else:
            old_k = json.loads(db[v].decode(encoding="utf8"))
            new_k = list(set([k, *old_k]))
            db[v] = json.dumps(new_k).encode(encoding="utf8")
    return [(f"MATCH (p:Publication) WHERE p.{args.key}=$value RETURN p.title", {"value": args.value})]


def rm_favorite_paper_args2querys(args: object):
    username = args.username
    favorites_paper_path = os.path.join(favorites_dirname, username, "papers")
    os.makedirs(os.path.dirname(favorites_paper_path), exist_ok=True)
    k, v = args.key, args.value.encode(encoding="utf8")
    with dbm.open(favorites_paper_path, 'c') as db:
        if v in db:
            old_k = set(json.loads(db[v].decode(encoding="utf8")))
            if k in old_k:
                old_k.remove(k)
                new_k = list(old_k)
                if len(new_k) <= 0:
                    del db[v]
                else:
                    db[v] = json.dumps(new_k).encode(encoding="utf8")
    return [(f"MATCH (p:Publication) WHERE p.{args.key}=$value RETURN p.title", {"value": args.value})]


def add_favorite_paper_results2message(res, args: object):
    msg = f"Paper added in favorites. {args.key}:{args.value}"
    for r in res[0]:
        msg += "\n" + f"<b>{r[0]}</b>"
    return msg, [[
        InlineKeyboardButton(
            f'Remove it',
            switch_inline_query_current_chat=f'/rm_favorite_paper "{args.key}" "{args.value}"'),
        InlineKeyboardButton(
            f'Show all',
            switch_inline_query_current_chat=f'/show_favorite_paper -o date')
    ]]


def rm_favorite_paper_results2message(res, args: object):
    msg = f"Paper removed from favorites. {args.key}:{args.value}"
    for r in res[0]:
        msg += "\n" + f"<b>{r[0]}</b>"
    return msg, [[
        InlineKeyboardButton(
            f'Revoke it',
            switch_inline_query_current_chat=f'/add_favorite_paper "{args.key}" "{args.value}"'),
        InlineKeyboardButton(
            f'Show all',
            switch_inline_query_current_chat=f'/show_favorite_paper -o date')
    ]]


add_favorite_paper_jump = Jump(
    name="add_favorite_paper",
    parser_add_arguments=favorite_paper_parser_add_arguments,
    args2querys=add_favorite_paper_args2querys,
    results2message=add_favorite_paper_results2message,
    description=None
)


rm_favorite_paper_jump = Jump(
    name="rm_favorite_paper",
    parser_add_arguments=favorite_paper_parser_add_arguments,
    args2querys=rm_favorite_paper_args2querys,
    results2message=rm_favorite_paper_results2message,
    description=None
)


def favorite_paper_args2querys(args: object):
    username = args.username
    favorites_paper_path = os.path.join(favorites_dirname, username, "papers")
    os.makedirs(os.path.dirname(favorites_paper_path), exist_ok=True)
    pwhere, jwhere, orderby, limits, values = parse_args_papers(args)
    k_or, v_or = [], {}
    with dbm.open(favorites_paper_path, 'c') as db:
        i = 0
        for v in db.keys():
            ks = db[v]
            for k in json.loads(ks.decode("utf8")):
                k_or.append(f"p.{k}=$fav{i}")
                v_or[f"fav{i}"] = v.decode("utf8")
                i += 1
    if len(k_or) <= 0:
        return []
    pwhere += " AND " + f"({' or '.join(k_or)})"
    values = {**values, **v_or}
    return [(
        f"MATCH (p:Publication) WHERE {pwhere} " +
        ("OPTIONAL MATCH (p:Publication)-[:PUBLISH]->(j:Journal) " if jwhere == '' else f"MATCH (p:Publication)-[:PUBLISH]->(j:Journal) WHERE {jwhere} ") +
        f"OPTIONAL MATCH (c:Publication)-[:CITE]->(p:Publication) "
        f"OPTIONAL MATCH (r:Publication)<-[:CITE]-(p:Publication) "
        f"RETURN p, j, COUNT(DISTINCT c) AS citation, COUNT(DISTINCT r) AS reference ORDER BY {orderby} LIMIT {limits}",
        {**values}
    )]


show_favorite_paper_jump = Jump(
    name="show_favorite_paper",
    parser_add_arguments=add_arguments_papers,
    args2querys=favorite_paper_args2querys,
    results2message=papers_results2message,
    description=Description(help="Show my favorite papers", default_args="-o date")
)


def add_favorite_keywords_args2querys(args: object):
    username = args.username
    favorites_keywords_path = os.path.join(favorites_dirname, username, "keywords")
    os.makedirs(os.path.dirname(favorites_keywords_path), exist_ok=True)
    with dbm.open(favorites_keywords_path, 'c') as db:
        for keyword in args.keyword:
            db[keyword.encode(encoding="utf8")] = ''
    return [(f"RETURN true", {})]


def show_favorite_keywords_results2message(_, args: object):
    username = args.username
    favorites_keywords_path = os.path.join(favorites_dirname, username, "keywords")
    os.makedirs(os.path.dirname(favorites_keywords_path), exist_ok=True)
    msg = "Your favorited keywords:"
    keyboard = []
    with dbm.open(favorites_keywords_path, 'c') as db:
        for keyword in db.keys():
            keyword = keyword.decode(encoding="utf8")
            msg += "\n" + f"<b>{keyword}</b>"
            keyboard.append([
                InlineKeyboardButton(
                    f'Use "{keyword}"',
                    switch_inline_query_current_chat=f'/search_by_title -k "{keyword}" -o date'),
                InlineKeyboardButton(
                    f'Remove "{keyword}"',
                    switch_inline_query_current_chat=f'/rm_favorite_keywords -k "{keyword}"')
            ])
    return msg, keyboard


add_favorite_keywords_jump = Jump(
    name="add_favorite_keywords",
    parser_add_arguments=add_arguments_papers,
    args2querys=add_favorite_keywords_args2querys,
    results2message=show_favorite_keywords_results2message,
    description=None
)


show_favorite_keywords_jump = Jump(
    name="show_favorite_keywords",
    parser_add_arguments=None,
    args2querys=lambda _: [(f"RETURN true", {})],
    results2message=show_favorite_keywords_results2message,
    description=Description(help="Show my favorite keywords", default_args="")
)


def rm_favorite_keywords_args2querys(args: object):
    username = args.username
    favorites_keywords_path = os.path.join(favorites_dirname, username, "keywords")
    os.makedirs(os.path.dirname(favorites_keywords_path), exist_ok=True)
    with dbm.open(favorites_keywords_path, 'c') as db:
        for keyword in args.keyword:
            if keyword.encode(encoding="utf8") in db:
                del db[keyword.encode(encoding="utf8")]
    return [(f"RETURN true", {})]


def rm_favorite_keywords_results2message(_, args: object):
    msg = "The following keywords removed:"
    keyboard = []
    for keyword in args.keyword:
        msg += "\n" + f"<b>{keyword}</b>"
        keyboard.append([
            InlineKeyboardButton(
                f'Revoke "{keyword}"',
                switch_inline_query_current_chat=f'/add_favorite_keywords -k "{keyword}"'),
            InlineKeyboardButton(
                f'Show all',
                switch_inline_query_current_chat=f'/show_favorite_keywords')
        ])
    return msg, keyboard


rm_favorite_keywords_jump = Jump(
    name="rm_favorite_keywords",
    parser_add_arguments=add_arguments_papers,
    args2querys=rm_favorite_keywords_args2querys,
    results2message=rm_favorite_keywords_results2message,
    description=None
)
