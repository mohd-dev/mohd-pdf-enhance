##
#     Project: MOHD PDF Enhance
# Description: Apply various fixes to PDF files before processing them
#      Author: MOHD <it@mohd.it>
#   Copyright: 2023 MOHD
##
#
# Random result filter
#
##

import random
from typing import Any

def process(filename: str,
            destination: str,
            options: dict[str, Any]) -> bool:
    """
    Random filter which only returns a random result

    :param filename: source PDF file to process
    :param destination: destination PDF file to write the output
    :param options: dictionary with options
    :return: process status
    """
    return bool(random.randint(0, 1))
