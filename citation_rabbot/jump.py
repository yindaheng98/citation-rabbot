from typing import Callable, Tuple, Dict
from neo4j import Session, Result
from telegram import Update
from telegram.ext import Application, ContextTypes, CommandHandler


class Rabbot:
    def __init__(self, bot: Application, session: Session) -> None:
        self.bot = bot
        self.session = session

    def set_jump(self, name: str, message2query: Callable[[str], Tuple[str, Dict]], result2message: Callable[[Result], str]):
        async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
            text = update.message
            query, kwargs = message2query(text)
            result = self.session.execute_read(lambda tx: tx.run(query, **kwargs))
            message = result2message(result)
            await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

        command_handler = CommandHandler(name, handler)
        self.bot.add_handler(command_handler)
