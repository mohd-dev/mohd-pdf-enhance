##
#     Project: MOHD PDF Enhance
# Description: Apply various fixes to PDF files before processing them
#      Author: MOHD <it@mohd.it>
#   Copyright: 2023 MOHD
##

import logging
from typing import Union


def setup_logging(level: Union[str, int]) -> None:
    """
    Set up logging
    """
    logging.basicConfig(level=level,
                        format='%(asctime)s '
                               '%(levelname)-8s '
                               '%(filename)-25s '
                               'line: %(lineno)-5d '
                               '%(funcName)-30s '
                               'pid: %(process)-9d '
                               '%(message)s')
    logging.debug(f'Logging level set to: {level}')
