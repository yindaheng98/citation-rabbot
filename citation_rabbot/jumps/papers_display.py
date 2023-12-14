from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from typing import List


def papers_results2message(res: List, args: object):
    msg = ""
    keyboard = []
    for i, (paper, journal, cited) in enumerate(res[0]):
        title = paper['title']
        info = f"{journal['dblp_name']} (CCF {journal['ccf']}),{paper['year']}"
        if "doi" in paper:
            msg += f'{i+1}: <b>{cited}</b> cited: <a href="https://doi.org/{paper["doi"]}">{title}</a>,{info}\n'
        else:
            msg += f"{i+1}: <b>{cited}</b> cited: {title},{info}\n"
        keyboard.append([
            InlineKeyboardButton(
                f"{i+1}'s Authors",
                switch_inline_query_current_chat=f"/paper_authors title_hash:{paper['title_hash']}"),
            InlineKeyboardButton(
                f"{i+1}'s Citations",
                switch_inline_query_current_chat=f"/citations title_hash:{paper['title_hash']}"),
            InlineKeyboardButton(
                f"{i+1}'s References",
                switch_inline_query_current_chat=f"/references title_hash:{paper['title_hash']}"),
        ])
    if msg == "":
        msg = "No papers yet"
    return msg, InlineKeyboardMarkup(keyboard)
