from typing import Tuple, Dict, List
from telegram import InlineKeyboardButton
from .models import Description


def start_args2querys(_) -> List[Tuple[str, Dict]]:
    return [
        ("MATCH ()-[r]->() RETURN type(r), COUNT(*)", {}),
        ("MATCH (n) RETURN labels(n), COUNT(n)", {})
    ]


def gen_start_results2message(names, desc_dict):
    keyboards = []
    for name in names:
        desc = desc_dict[name]
        cmd = "-h"
        if isinstance(desc, Description):
            desc, cmd = desc.help, desc.default_args
        keyboards.append([InlineKeyboardButton(desc, switch_inline_query_current_chat=f"/{name} {cmd}")])

    def start_results2message(res: List, _):
        msg = "I'm jumping! Here is the places I'm jumping:\n"
        edge_counts, node_counts = res
        msg += "This place has lots of nodes:\n"
        for name, count in node_counts:
            msg += f"{count} {name} nodes\n"
        msg += "And lots of edges:\n"
        for name, count in edge_counts:
            msg += f"{count} {name} edges\n"
        msg += 'Want to know what I really is? Here is <a href="https://github.com/yindaheng98/citation-rabbot">my code</a>\n'
        msg += 'To start jump, you may want to:'
        return msg, keyboards
    return start_results2message
