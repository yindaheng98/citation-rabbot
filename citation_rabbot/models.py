from argparse import ArgumentParser
from typing import Callable, Tuple, Dict, List, Sequence, NamedTuple, Optional
from telegram import InlineKeyboardButton


class ObjArgs(NamedTuple):
    username: str
    # Add more in future


class Description(NamedTuple):
    help: str
    default_args: str


class Jump(NamedTuple):
    name: str
    parser_add_arguments: Optional[Callable[[ArgumentParser], ArgumentParser]]
    args2querys: Callable[[object], List[Tuple[str, Dict]]]
    results2message: Callable[[List, object], Tuple[str, Sequence[Sequence[InlineKeyboardButton]]]]
    description: Optional[str | Description]
