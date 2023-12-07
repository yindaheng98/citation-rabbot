import argparse
import importlib
from .jumps import *


def add_argument_jump(parser: argparse.ArgumentParser, *flags, dest: str = 'jump') -> None:
    if len(flags) <= 0:
        flags = ['-j', '--jump']
    parser.add_argument(
        *flags, dest=dest, action='append', required=False, default=[],
        help=f'A jump! (a tuple: <name>,<message2query>,<result2message>).'
    )


def parse_args_jump(parser: argparse.ArgumentParser, jump_dest: str = 'jump'):
    args = parser.parse_args()
    jump_list = []
    for jump_s in args.__getattribute__(jump_dest):
        jump = eval(jump_s)
        if isinstance(jump, tuple):
            jump_list.append(jump)
    return jump_list
