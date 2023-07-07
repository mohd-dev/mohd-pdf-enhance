##
#     Project: MOHD PDF Enhance
# Description: Apply various fixes to PDF files before processing them
#      Author: MOHD <it@mohd.it>
#   Copyright: 2023 MOHD
##
#
# Dummy filter
#
##

from typing import Any

def process(filename: str,
            destination: str,
            options: dict[str, Any]) -> bool:
    """
    Dummy filter which only returns the status from the options

    :param filename: source PDF file to process
    :param destination: destination PDF file to write the output
    :param options: dictionary with options
    :return: process status
    """
    return options['result-status']
