import asyncio
import re
import shlex
from argparse import ArgumentParser
from typing import Callable, Tuple, Dict, List
from neo4j import Session
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import filters, Application, ContextTypes, CommandHandler, MessageHandler
from telegram.constants import ParseMode


class Rabbot:
    def __init__(self, app: Application, session: Session) -> None:
        self.app = app
        self.session = session
        self.bot_name = None

    async def _fetch_name(self):
        me = await self.app.bot.get_me()
        self.bot_name = me.name

    def add_jump(self, name: str,
                 parser: ArgumentParser,
                 args2querys: Callable[[str], List[Tuple[str, Dict]]],
                 results2message: Callable[[List], Tuple[str, InlineKeyboardMarkup]]):
        async def handler(text: str, update: Update, context: ContextTypes.DEFAULT_TYPE):
            lst_args = []
            str_args = re.findall(r"^/[A-Za-z_]+ *(.*)$", text)
            obj_args = None
            if len(str_args) > 0:
                lst_args = shlex.split(str_args[0])
            if parser:
                parser.exit_on_error = False
                obj_args = parser.parse_args(lst_args)
            querys = args2querys(obj_args)
            if not querys or len(querys) <= 0:
                return
            results = []
            for query, kwargs in querys:
                results.append(self.session.execute_read(lambda tx: tx.run(query, **kwargs).values()))
            message, reply_markup = results2message(results)
            await update.message.reply_text(text=message, reply_to_message_id=update.message.id, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
        command_handler = CommandHandler(name, lambda update, context: handler(update.message.text, update, context))
        self.app.add_handler(command_handler)

        if self.bot_name is None:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self._fetch_name())

        async def wrap_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
            split = re.findall(f"^{self.bot_name} +(/{name} +.*)", update.message.text)
            if len(split) > 0:
                await handler(split[0], update, context)
        message_handler = MessageHandler(filters.Regex(f"^{self.bot_name} +/{name}"), wrap_handler)
        self.app.add_handler(message_handler)
