import argparse
import logging
from neo4j import GraphDatabase
from telegram.ext import ApplicationBuilder
from .arg import add_argument_jump, parse_args_jump
from .rabbot import Rabbot
from .start import start_message2querys, start_results2message
from .jumps import paper_authors_jump, author_papers_jump, citations_jump, references_jump, search_by_title_jump
default_jumps = [
    paper_authors_jump, author_papers_jump, citations_jump, references_jump, search_by_title_jump
]
default_jumps_name = [
    "start_jump", "paper_authors_jump", "author_papers_jump", "citations_jump", "references_jump", "search_by_title_jump"
]
defaults_desc = "".join([" -j "+name for name in default_jumps_name])
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

parser = argparse.ArgumentParser()

parser.add_argument("--auth", type=str, default=None, help=f'Auth to neo4j database.')
parser.add_argument("--uri", type=str, required=True, help=f'URI to neo4j database.')
parser.add_argument("--token", type=str, required=True, help=f'Telegram bot token.')
add_argument_jump(parser, defaults_desc=defaults_desc)


args = parser.parse_args()
jump_list = parse_args_jump(parser)


jump_dict = {name: (message2query, result2message) for name, message2query, result2message, _ in jump_list}
desc_dict = {name: desc for name, _, _, desc in jump_list if desc}
desc_name = [name for name, _, _, desc in jump_list if desc]
for name, message2query, result2message, desc in default_jumps:
    if name not in jump_dict:
        jump_dict[name] = (message2query, result2message)
    if desc:
        desc_dict[name] = desc
        desc_name.append(name)

application = ApplicationBuilder().token(args.token).build()
with GraphDatabase.driver(args.uri, auth=args.auth) as driver:
    with driver.session() as session:
        rabbot = Rabbot(app=application, session=session)
        for name, (message2query, result2message) in jump_dict.items():
            rabbot.add_jump(name, message2query, result2message)
        rabbot.add_jump('start', start_message2querys, start_results2message)
        application.run_polling()
