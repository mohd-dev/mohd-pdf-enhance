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
import subprocess
import sys
import tempfile


try:
    from mohd_pdf_enhance.utility.command_line_arguments import (
        CommandLineArguments)
    from mohd_pdf_enhance.utility.setup_logging import setup_logging
except ModuleNotFoundError:
    # Fix module search path adding the current directory
    # Mostly needed for embedded Python
    sys.path.append('.')
    from mohd_pdf_enhance.utility.command_line_arguments import (
        CommandLineArguments)
    from mohd_pdf_enhance.utility.setup_logging import setup_logging


def get_options():
    """
    Get command line arguments

    :return: Parsed options from command line
    """
    arguments = CommandLineArguments()
    arguments.parser.add_argument('--settings',
                                  type=str,
                                  required=False,
                                  help='Settings file')
    arguments.parser.add_argument('filename',
                                  type=str,
                                  nargs=1,
                                  help='PDF file to process')
    arguments.parser.add_argument('--temp',
                                  action='store_true',
                                  required=False,
                                  help='Save the result in a temporary file')
    arguments.parse_arguments()
    # Check the settings argument
    if not arguments.options.settings:
        parent_dir = pathlib.Path(__file__).parent
        if not (parent_dir / 'settings.json').is_file():
            parent_dir = parent_dir.parent
        arguments.options.settings = parent_dir / 'settings.json'
    if not pathlib.Path(arguments.options.settings).exists():
        arguments.parser.error(f'Settings file "{arguments.options.settings}" '
                               f'does not exists')
    # Check the filename argument
    if not pathlib.Path(arguments.options.filename[0]).exists():
        arguments.parser.error(f'PDF file "{arguments.options.filename[0]}" '
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
    destination_filename = tempfile.mktemp(suffix='.pdf')
    shutil.copy(src=options.filename[0],
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
    # Save upon the original file if requested
    if not options.temp:
        shutil.copy(src=destination_filename,
                    dst=options.filename[0])
        destination_filename = options.filename[0]
    # At the end of the processing execute the post execute command
    post_command = settings.get('post-execute').format(
        FILENAME=destination_filename)
    if post_command:
        logging.info(f'Executing post-execute command: "{post_command}"')
        subprocess.run(args=post_command,
                       shell=True)
    logging.debug('Process ended')


if __name__ == '__main__':
    main()
