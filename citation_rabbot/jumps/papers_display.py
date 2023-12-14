from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from typing import List


def reconstruct_paper_args(args: object):
    paper_args = ""
    paper_args += f"--order {args.order} "
    # paper_args += f"--year {args.year} "
    # paper_args += ' '.join([f'--keyword "{k}"' for k in args.keyword]) + " "
    # paper_args += ' '.join([f'--key_value "{kv}"' for kv in args.key_value]) + " "
    paper_args += f"--limit {args.limit}"
    return paper_args


def papers_results2message(res: List, args: object):
    msg = ""
    paper_args = reconstruct_paper_args(args)
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
                switch_inline_query_current_chat=f"/paper_authors {paper_args} title_hash {paper['title_hash']}"),
            InlineKeyboardButton(
                f"{i+1}'s Citations",
                switch_inline_query_current_chat=f"/citations {paper_args} title_hash {paper['title_hash']}"),
            InlineKeyboardButton(
                f"{i+1}'s References",
                switch_inline_query_current_chat=f"/references {paper_args} title_hash {paper['title_hash']}"),
        ])
    if msg == "":
        msg = "No papers yet"
    return msg, InlineKeyboardMarkup(keyboard)
