from typing import Callable, Tuple, Dict, List
from neo4j import Session
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import Application, ContextTypes, CommandHandler


class Rabbot:
    def __init__(self, bot: Application, session: Session) -> None:
        self.bot = bot
        self.session = session

    def add_jump(self, name: str, message2querys: Callable[[str], List[Tuple[str, Dict]]], results2message: Callable[[List], Tuple[str, InlineKeyboardMarkup]]):
        async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
            querys = message2querys(update.message)
            if not querys or len(querys) <= 0:
                return
            results = []
            for query, kwargs in querys:
                results.append(self.session.execute_read(lambda tx: tx.run(query, **kwargs).values()))
            message, reply_markup = results2message(results)
            await update.message.reply_text(text=message, reply_markup=reply_markup)

        command_handler = CommandHandler(name, handler)
        self.bot.add_handler(command_handler)
