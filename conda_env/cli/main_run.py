from argparse import RawDescriptionHelpFormatter
import os

from conda import config
from conda.cli import common
from ..run import env_run


description = """
Run a program inside a given conda environment.
"""

example = """
examples:
    conda env run foo ipython
    conda env run foo ipython -- notebook /path/to/notebook.ipynb
"""

def configure_parser(sub_parsers):
    p = sub_parsers.add_parser(
        'run',
        formatter_class=RawDescriptionHelpFormatter,
        description=description,
        help=description,
        epilog=example,
    )

    p.add_argument(
        'environment',
        action='store',
        help='name of environment (in %s)' % os.pathsep.join(config.envs_dirs),
    )

    p.add_argument(
        'program',
        action='store',
        help='name of the program to run',
    )

    p.add_argument(
        'arguments',
        action='store',
        nargs='*',
        help='arguments to pass to the program',
        default=None,
    )

    p.add_argument(
        '-q', '--quiet',
        default=False,
    )
    common.add_parser_json(p)
    p.set_defaults(func=execute)

def execute(args, parser):
    env_run(args.environment, args.program, args.arguments)
