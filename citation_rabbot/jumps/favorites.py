import dbm
import os
import json
from telegram import InlineKeyboardButton
from .papers_args import add_arguments_papers

favorites_dirname = "save/favorites"


def add_favorite_paper_parser_add_arguments(parser):
    parser.add_argument('key', metavar='key', type=str,
                        help='Key and value to identify the paper')
    parser.add_argument('value', metavar='value', type=str,
                        help='Key and value to identify the paper')
    return parser


def add_favorite_paper_args2querys(args: object):
    username = args.update.message.from_user.username
    favorites_paper_path = os.path.join(favorites_dirname, username, "papers")
    os.makedirs(os.path.dirname(favorites_paper_path), exist_ok=True)
    with dbm.open(favorites_paper_path, 'c') as db:
        if args.value not in db:
            db[args.value.encode(encoding="utf8")] = json.dumps([args.key]).encode(encoding="utf8")
        else:
            old_value = json.loads(db[args.value.encode(encoding="utf8")].decode(encoding="utf8"))
            new_value = list(set([args.key, *old_value]))
            db[args.value.encode(encoding="utf8")] = json.dumps(new_value).encode(encoding="utf8")
    return [(f"MATCH (p:Publication) WHERE p.{args.key}=$value RETURN p.title", {"value": args.value})]


def add_favorite_paper_results2message(res, args: object):
    msg = f"Paper added in favorites.\n{args.key}:{args.value}:"
    for r in res[0]:
        msg += "\n" + r[0]
    return msg, []


add_favorite_paper_jump = (
    "add_favorite_paper",
    add_favorite_paper_parser_add_arguments,
    add_favorite_paper_args2querys,
    add_favorite_paper_results2message,
    None
)


def add_favorite_keywords_args2querys(args: object):
    username = args.update.message.from_user.username
    favorites_keywords_path = os.path.join(favorites_dirname, username, "keywords")
    os.makedirs(os.path.dirname(favorites_keywords_path), exist_ok=True)
    with dbm.open(favorites_keywords_path, 'c') as db:
        for keyword in args.keyword:
            db[keyword.encode(encoding="utf8")] = ''
    return [(f"RETURN true", {})]


def show_favorite_keywords_results2message(_, args: object):
    username = args.update.message.from_user.username
    favorites_keywords_path = os.path.join(favorites_dirname, username, "keywords")
    os.makedirs(os.path.dirname(favorites_keywords_path), exist_ok=True)
    msg = "Your favorited keywords:"
    keyboard = []
    with dbm.open(favorites_keywords_path, 'c') as db:
        for keyword in db:
            keyword = keyword.decode(encoding="utf8")
            msg += "\n" + keyword
            keyboard.append([
                InlineKeyboardButton(
                    f'Use "{keyword}"',
                    switch_inline_query_current_chat=f'/search_by_title -k "{keyword}"'),
                InlineKeyboardButton(
                    f'Remove "{keyword}"',
                    switch_inline_query_current_chat=f'/rm_favorite_keywords -k "{keyword}"')
            ])
    return msg, keyboard


add_favorite_keywords_jump = (
    "add_favorite_keywords",
    add_arguments_papers,
    add_favorite_keywords_args2querys,
    show_favorite_keywords_results2message,
    None
)


show_favorite_keywords_jump = (
    "show_favorite_keywords",
    None,
    lambda _: [(f"RETURN true", {})],
    show_favorite_keywords_results2message,
    "Show your favorite keywords"
)
