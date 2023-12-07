from typing import Callable, Tuple, Dict, List
from neo4j import Session
from telegram import Update
from telegram.ext import Application, ContextTypes, CommandHandler


class Rabbot:
    def __init__(self, bot: Application, session: Session) -> None:
        self.bot = bot
        self.session = session

    def add_jump(self, name: str, message2querys: Callable[[str], List[Tuple[str, Dict]]], results2message: Callable[[List], str]):
        async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
            text = update.message
            querys = message2querys(text)
            if not querys or len(querys) <= 0:
                return
            results = []
            for query, kwargs in querys:
                results.append(self.session.execute_read(lambda tx: tx.run(query, **kwargs).values()))
            message = results2message(results)
            await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

        command_handler = CommandHandler(name, handler)
        self.bot.add_handler(command_handler)
