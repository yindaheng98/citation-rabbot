from typing import Tuple, Dict
from neo4j import Result


def test_message2query(msg: str) -> Tuple[str, Dict]:
    pass


def test_result2message(res: Result) -> str:
    pass


test_jump = ("test", test_message2query, test_result2message)
