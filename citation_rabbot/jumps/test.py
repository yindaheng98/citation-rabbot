from telegram import Message
from typing import Tuple, Dict, List
from neo4j import Result


def test_message2querys(msg: Message) -> List[Tuple[str, Dict]]:
    pass


def test_results2message(res: List[Result]) -> str:
    pass


test_jump = ("test", test_message2querys, test_results2message)
