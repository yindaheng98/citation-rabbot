import argparse
import importlib
from .jumps import *


def add_argument_jump(parser: argparse.ArgumentParser, *flags, dest: str = 'jump', defaults_desc="") -> None:
    if len(flags) <= 0:
        flags = ['-j', '--jump']
    parser.add_argument(
        *flags, dest=dest, action='append', required=False, default=[],
        help=f'A jump! Variable name of a python tuple: <name>,<args2querys>,<results2message>,<description>. '
        'If you set <description>, the command will become explict (show in chat by set_my_commands '
        'like https://stackoverflow.com/questions/62607644/bot-set-my-command-using-this-function-how-to-set-commands-and-how-to-pass-arg). '
        'Default: '+defaults_desc
    )


def parse_args_jump(parser: argparse.ArgumentParser, jump_dest: str = 'jump'):
    args = parser.parse_args()
    jump_list = []
    for jump_s in args.__getattribute__(jump_dest):
        jump = eval(jump_s)
        if isinstance(jump, tuple):
            jump_list.append(jump)
    return jump_list
