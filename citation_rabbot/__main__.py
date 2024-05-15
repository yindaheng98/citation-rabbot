import argparse
import logging
from neo4j import GraphDatabase
from telegram.ext import Application, ApplicationBuilder
from .arg import add_argument_jump, parse_args_jump
from .rabbot import Rabbot, Jump
from .start import start_args2querys, gen_start_results2message
from .jumps import *
default_jumps_name = [
    "author_papers_jump", "citations_jump", "references_jump",
    "search_by_title_jump", "search_by_title_semantic_jump", "search_by_abstract_semantic_jump",
    "paper_detail_jump",
    "add_favorite_paper_jump", "show_favorite_paper_jump", "rm_favorite_paper_jump",
    "add_favorite_keywords_jump", "show_favorite_keywords_jump", "rm_favorite_keywords_jump"
]
default_jumps = [eval(name) for name in default_jumps_name]
default_jumps_name = ["start_jump", *default_jumps_name]
defaults_desc = "".join([" -j "+name for name in default_jumps_name])
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

parser = argparse.ArgumentParser()

parser.add_argument("--username", type=str, default=None, help=f'Auth username to neo4j database.')
parser.add_argument("--password", type=str, default=None, help=f'Auth password to neo4j database.')
parser.add_argument("--uri", type=str, required=True, help=f'URI to neo4j database.')
parser.add_argument("--token", type=str, required=True, help=f'Telegram bot token.')
add_argument_jump(parser, defaults_desc=defaults_desc)


args = parser.parse_args()
jump_list = parse_args_jump(parser)

# Parse jump list
jump_dict = {jump.name: jump for jump in jump_list}
desc_dict = {jump.name: jump.description for jump in jump_list if jump.description}
desc_order = [jump.name for jump in jump_list if jump.description]
# Add default jumps
for jump in default_jumps:
    if jump.name not in jump_dict:
        jump_dict[jump.name] = jump
    if jump.description:
        desc_dict[jump.name] = jump.description
        desc_order.append(jump.name)


async def post_init(application: Application):
    await application.bot.set_my_commands([('start', "Let's jump!")])
application = ApplicationBuilder().token(args.token).post_init(post_init).build()

with GraphDatabase.driver(args.uri, auth=(args.username, args.password)) as driver:
    with driver.session() as session:
        rabbot = Rabbot(app=application, session=session)
        for name, jump in jump_dict.items():
            rabbot.add_jump(jump)
        rabbot.add_jump(Jump(
            name="start",
            parser_add_arguments=None,
            args2querys=start_args2querys,
            results2message=gen_start_results2message(desc_order, desc_dict),
            description=None
        ))
        application.run_polling()
