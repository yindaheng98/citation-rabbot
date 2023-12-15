from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from typing import List


def reconstruct_paper_args(args: object):
    paper_args = ""
    paper_args += f"--order {args.order} "
    paper_args += f"--year {args.year} "
    paper_args += ' '.join([f'--keyword "{k}"' for k in args.keyword]) + " "
    paper_args += ' '.join([f'--where_paper "{kv}"' for kv in args.where_paper]) + " "
    paper_args += ' '.join([f'--where_journal "{kv}"' for kv in args.where_journal]) + " "
    paper_args += f"--limit {args.limit}"
    return paper_args


def papers_results2message(res: List, args: object):
    msg = ""
    paper_args = reconstruct_paper_args(args)
    keyboards = []
    for i, (paper, journal, n_cite, n_refs) in enumerate(res[0]):
        title = paper['title']
        journal_info = "not published"
        if journal:
            journal_info = f"<i>{journal['dblp_name']}</i> (CCF {journal['ccf']})"
        msg += f'<b>P{i+1}.</b> '
        if "doi" in paper:
            msg += f'<a href="https://doi.org/{paper["doi"]}"><b>{title}</b></a>'
        else:
            msg += f"<b>{title}</b>"
        msg += f", {journal_info}, {paper['date'] if 'date' in paper else paper['year']}"
        msg += f", {n_refs} references, <b>{n_cite} citations</b>\n"

        keyboards.append(
            InlineKeyboardButton(
                f"P{i+1} Detail",
                switch_inline_query_current_chat=f"/paper_detail {paper_args} title_hash {paper['title_hash']}")
        )
    N = 3
    keyboard = []
    for i in range(len(keyboards) // N + 1):
        keyboard.append([])
        for j in range(N):
            if i*3+j < len(keyboards):
                keyboard[-1].append(keyboards[i*3+j])
    if msg == "":
        msg = "No papers yet"
    return msg, InlineKeyboardMarkup(keyboard)
