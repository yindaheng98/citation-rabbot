import argparse
import logging
from neo4j import GraphDatabase
from telegram.ext import ApplicationBuilder
from .arg import add_argument_jump, parse_args_jump
from .jump import Rabbot
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

parser = argparse.ArgumentParser()

parser.add_argument("--auth", type=str, default=None, help=f'Auth to neo4j database.')
parser.add_argument("--uri", type=str, required=True, help=f'URI to neo4j database.')
parser.add_argument("--token", type=str, required=True, help=f'Telegram bot token.')
add_argument_jump(parser)


args = parser.parse_args()
jump_list = parse_args_jump(parser)

application = ApplicationBuilder().token(args.token).build()
with GraphDatabase.driver(args.uri, auth=args.auth) as driver:
    rabbot = Rabbot(bot=application)
