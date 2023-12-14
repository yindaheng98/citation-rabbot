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
    keyboards = []
    for i, (paper, journal, cited) in enumerate(res[0]):
        title = paper['title']
        info = f"{journal['dblp_name']} (CCF {journal['ccf']}), {paper['date'] if 'date' in paper else paper['year']}"
        if "doi" in paper:
            msg += f'<b>{i+1}.</b> <a href="https://doi.org/{paper["doi"]}">{title}</a>, {info}, {cited} citations\n'
        else:
            msg += f"<b>{i+1}.</b> {title}, {info}, {cited} citations\n"

        keyboards.append(
            InlineKeyboardButton(
                f"{i+1}'s Detail",
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
