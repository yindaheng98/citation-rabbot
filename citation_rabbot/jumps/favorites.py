import dbm
import os
import json

favorites_dirname = "save/favorites"


def add_favorite_paper_parser_add_arguments(parser):
    parser.add_argument('key', metavar='key', type=str,
                        help='Key and value to identify the paper')
    parser.add_argument('value', metavar='value', type=str,
                        help='Key and value to identify the paper')
    return parser


favorites_paper_dirname = os.path.join(favorites_dirname, "papers")


def add_favorite_paper_args2querys(args: object):
    username = args.update.message.from_user.username
    favorites_paper_path = os.path.join(favorites_dirname, username, "papers")
    os.makedirs(os.path.dirname(favorites_paper_path), exist_ok=True)
    with dbm.open(favorites_paper_path, 'c') as db:
        if args.value not in db:
            db[args.value] = json.dumps([args.key])
        else:
            db[args.value] = json.dumps(list(set([args.key, *db[args.value]])))
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
