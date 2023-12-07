import argparse
import logging
from neo4j import GraphDatabase
from telegram.ext import CommandHandler, ApplicationBuilder
from .arg import add_argument_jump, parse_args_jump
from .rabbot import Rabbot
from .jumps import start_jump
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
    with driver.session() as session:
        rabbot = Rabbot(app=application, session=session)
        jump_dict = {name: (message2query, result2message) for name, message2query, result2message in jump_list}
        _, message2query, result2message = start_jump
        jump_dict['start'] = (message2query, result2message)
        for name, (message2query, result2message) in jump_dict.items():
            rabbot.add_jump(name, message2query, result2message)
        application.run_polling()
