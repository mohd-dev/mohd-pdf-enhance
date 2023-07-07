##
#     Project: MOHD PDF Enhance
# Description: Apply various fixes to PDF files before processing them
#      Author: MOHD <it@mohd.it>
#   Copyright: 2023 MOHD
##

import importlib
import json
import logging
import pathlib
import shutil
import tempfile

from utility.command_line_arguments import CommandLineArguments
from utility.setup_logging import setup_logging


def get_options():
    """
    Get command line arguments

    :return: Parsed options from command line
    """
    arguments = CommandLineArguments()
    arguments.parser.add_argument('--settings',
                                  type=str,
                                  required=True,
                                  help='Settings file')
    arguments.parser.add_argument('--filename',
                                  type=str,
                                  required=True,
                                  help='PDF file to process')
    arguments.parser.add_argument('--debug',
                                  action='store_true',
                                  required=False,
                                  help='Execute debug')
    arguments.parse_arguments()
    # Check the settings argument
    if not pathlib.Path(arguments.options.settings).exists():
        arguments.parser.error(f'Settings file "{arguments.options.settings}" '
                               f'does not exists')
    # Check the filename argument
    if not pathlib.Path(arguments.options.filename).exists():
        arguments.parser.error(f'PDF file "{arguments.options.filename}" '
                               f'does not exists')
    return arguments.options


def main():
    # Get command line options and setup logging
    options = get_options()
    setup_logging(options.logging)
    # Load settings
    with open(options.settings, 'r') as file:
        settings=json.load(fp=file)
    # Create destination filename
    destination_filename = (tempfile.mktemp(suffix='.pdf')
                            if not options.debug
                            else 'temp.pdf')
    shutil.copy(src=options.filename,
                dst=destination_filename)
    # Load all the fix modules
    modules = [importlib.import_module(item)
               for item
               in settings.get('modules', [])]
    # Apply all the desired fixes
    for module in modules:
        logging.info(f'Executing {module.__name__}.process')
        if module.process(filename=destination_filename,
                          destination=destination_filename,
                          options=settings.get(module.__name__, {})):
            logging.debug(f'Filter {module.__name__}.process was executed')
        else:
            logging.debug(f'Filter {module.__name__}.process was not executed')


if __name__ == '__main__':
    main()
