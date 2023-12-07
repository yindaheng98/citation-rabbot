import argparse
import logging
import importlib
from neo4j import GraphDatabase
from telegram.ext import ApplicationBuilder
from .jump import Rabbot
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

parser = argparse.ArgumentParser()

parser.add_argument("--auth", type=str, default=None, help=f'Auth to neo4j database.')
parser.add_argument("--uri", type=str, required=True, help=f'URI to neo4j database.')
parser.add_argument("--token", type=str, required=True, help=f'Telegram bot token.')
parser.add_argument("--jump", type=str, required=True, help=f'A jump! (a tuple: <name>,<message2query>,<result2message>).')

args = parser.parse_args()

application = ApplicationBuilder().token(args.token).build()
with GraphDatabase.driver(args.uri, auth=args.auth) as driver:
    rabbot = Rabbot(bot=application)
