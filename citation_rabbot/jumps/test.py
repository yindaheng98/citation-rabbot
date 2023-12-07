from telegram import Message
from typing import Tuple, Dict, List


def test_message2querys(msg: Message) -> List[Tuple[str, Dict]]:
    return [
        ("MATCH ()-[r]->() RETURN type(r), COUNT(*)", {}),
        ("MATCH (n) RETURN labels(n), COUNT(n)", {})
    ]


def test_results2message(res: List):
    msg = "I'm jumping! Here is the places I'm jumping:\n"
    edge_counts, node_counts = res
    msg += "This place has lots of nodes:\n"
    for name, count in node_counts:
        msg += f"{count} {name} nodes\n"
    msg += "And lots of edges:\n"
    for name, count in edge_counts:
        msg += f"{count} {name} edges\n"
    return msg, None


test_jump = ("test", test_message2querys, test_results2message)
