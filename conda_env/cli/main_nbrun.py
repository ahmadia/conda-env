from argparse import RawDescriptionHelpFormatter
from os.path import basename
import json
import textwrap

from conda.cli import common
from conda.cli import install
from ..run import env_run

description = """
Run a notebook inside its conda environment.
"""

example = """
examples:
    conda env nbrun /path/to/notebook.ipynb
"""

def configure_parser(sub_parsers):
    p = sub_parsers.add_parser(
        'nbrun',
        formatter_class=RawDescriptionHelpFormatter,
        description=description,
        help=description,
        epilog=example,
    )

    p.add_argument(
        'notebook',
        action='store',
        help='path to the notebook containing a conda environment',
    )
    common.add_parser_install(p)
    common.add_parser_json(p)
    p.set_defaults(func=execute)

def extract_conda_profile(nb_path):
    nb_json = {}
    try:
        nb_json = json.load(open(nb_path))
    except (IOError, TypeError):
        msg = 'Unable to load notebook: %s\n\n' % nb_path
        msg += "\n".join(textwrap.wrap(textwrap.dedent("""
            Please verify that the above notebook is present, that you have
            permission to read the notebook's contents, and that it is a valid
            IPython or Jupyter Notebook file.""").lstrip()))
        common.error_and_exit(msg)
    try:
        environment = nb_json['metadata']['environment']
        provider = environment['provider']
        assert provider == 'conda'
        return environment['profile']
    except (KeyError, AssertionError):
        msg = 'No conda environment in notebook: %s\n\n' % e.filename
        msg += "\n".join(textwrap.wrap(textwrap.dedent("""
            Please verify that the notebook contains a valid conda environment
            in its metadata.""").lstrip()))

        common.error_and_exit(msg)

def profile_to_environment(profile, args, parser):
    args.name = basename(args.notebook)
    args.packages = profile['dependencies'] + ['ipython']
    args.clone = False
    args.no_default_packages = False
    install.install(args, parser, 'create')
    return args.name

def execute(args, parser):
    profile = extract_conda_profile(args.notebook)
    environment = profile_to_environment(profile, args, parser)
    program = "ipython"
    arguments = ["notebook", args.notebook]
    env_run(environment, program, arguments)