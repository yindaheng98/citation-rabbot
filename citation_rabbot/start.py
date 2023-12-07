from typing import Tuple, Dict, List


def start_message2querys(_) -> List[Tuple[str, Dict]]:
    return [
        ("MATCH ()-[r]->() RETURN type(r), COUNT(*)", {}),
        ("MATCH (n) RETURN labels(n), COUNT(n)", {})
    ]


def start_results2message(res: List):
    msg = "I'm jumping! Here is the places I'm jumping:\n"
    edge_counts, node_counts = res
    msg += "This place has lots of nodes:\n"
    for name, count in node_counts:
        msg += f"{count} {name} nodes\n"
    msg += "And lots of edges:\n"
    for name, count in edge_counts:
        msg += f"{count} {name} edges\n"
    msg += 'Want to know what I really is? Here is <a href="https://github.com/yindaheng98/citation-rabbot">my code</a>'
    return msg, None
