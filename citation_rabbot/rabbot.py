import asyncio
import re
import shlex
from argparse import ArgumentParser
from neo4j import Session
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import filters, Application, ContextTypes, CommandHandler, MessageHandler
from telegram.constants import ParseMode
from .models import Jump, ObjArgs


class Rabbot:
    def __init__(self, app: Application, session: Session) -> None:
        self.app = app
        self.session = session
        self.bot_name = None

    async def _fetch_name(self):
        me = await self.app.bot.get_me()
        self.bot_name = me.name

    def add_jump(self, jump: Jump):
        name = jump.name
        parser_add_arguments = jump.parser_add_arguments
        args2querys = jump.args2querys
        results2message = jump.results2message
        parser = ArgumentParser(add_help=False, exit_on_error=False)
        parser.add_argument('-h', '--help', action='store_true', help='Show help message.')
        if parser_add_arguments:
            parser = parser_add_arguments(parser)

        async def handler(text: str, update: Update, context: ContextTypes.DEFAULT_TYPE):
            lst_args = []
            str_args = re.findall(r"^/[A-Za-z_]+ *(.*)$", text)
            obj_args = None
            if len(str_args) > 0:
                lst_args = shlex.split(str_args[0])
            if parser_add_arguments is not None:
                if len(lst_args) <= 0 or '-h' in lst_args or '--help' in lst_args:
                    message = re.sub(r"^usage: __main__.py", f"usage: /{name}", parser.format_help())
                    await update.message.reply_text(text=message, reply_to_message_id=update.message.id)
                    return
                else:
                    obj_args = parser.parse_args(lst_args)
                    if not hasattr(obj_args, "username"):
                        setattr(obj_args, "username", update.message.from_user.username)
            else:
                obj_args = ObjArgs(username=update.message.from_user.username)
            querys = args2querys(obj_args)
            if not querys or len(querys) <= 0:
                return
            results = []
            for query, kwargs in querys:
                results.append(self.session.execute_read(lambda tx: tx.run(query, **kwargs).values()))
            message, keyboard = results2message(results, obj_args)
            reply_markup = InlineKeyboardMarkup([
                *keyboard, [InlineKeyboardButton(
                    "Try again",
                    switch_inline_query_current_chat=f"/{name} {str_args[0] if len(str_args) > 0 else ''}"
                )]
            ])
            await update.message.reply_text(text=message, reply_to_message_id=update.message.id, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
        command_handler = CommandHandler(name, lambda update, context: handler(update.message.text, update, context))
        self.app.add_handler(command_handler)

        if self.bot_name is None:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self._fetch_name())

        async def wrap_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
            split = re.findall(f"^{self.bot_name} +(/{name} *.*)", update.message.text)
            if len(split) > 0:
                await handler(split[0], update, context)
        message_handler = MessageHandler(filters.Regex(f"^{self.bot_name} +/{name} "), wrap_handler)
        self.app.add_handler(message_handler)
        message_handler = MessageHandler(filters.Regex(f"^{self.bot_name} +/{name}$"), wrap_handler)
        self.app.add_handler(message_handler)
