##
#     Project: MOHD PDF Enhance
# Description: Apply various fixes to PDF files before processing them
#      Author: MOHD <it@mohd.it>
#   Copyright: 2023 MOHD
##

import argparse
import logging


class CommandLineArguments(object):
    """
    Parse command line arguments adding some methods to add a group of
    """
    GROUP_ODOO = 'Odoo'
    GROUP_OPTIONS = 'Options'

    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('--logging',
                                 type=str,
                                 required=False,
                                 choices=logging._nameToLevel.keys(),
                                 default=logging._levelToName[logging.INFO],
                                 help='Logging level')
        self.options = None
        self.groups = {}

    def parse_arguments(self) -> None:
        """
        Parse command line arguments
        """
        self.options = self.parser.parse_args()

    def add_group(self, name: str) -> argparse._ArgumentGroup:
        """
        Add an arguments group

        :param name: group name
        :return: options group
        """
        group = self.parser.add_argument_group(name)
        self.groups[name] = group
        return group

    def get_group(self, name: str) -> argparse._ArgumentGroup:
        """
        Get an argument group from its name
        :param name: group name to get
        :return: options group
        """
        return self.groups[name]

    def add_args_odoo(self) -> None:
        """
        Add arguments for Odoo
        """
        group = self.add_group(self.GROUP_ODOO)
        group.add_argument('--odoo_url',
                           type=str,
                           help='Odoo URL for REST API',
                           required=True)
        group.add_argument('--odoo_database',
                           type=str,
                           help='Odoo database',
                           required=True)
        group.add_argument('--odoo_username',
                           type=str,
                           help='Odoo username',
                           required=True)
        group.add_argument('--odoo_password',
                           type=str,
                           help='Odoo password for the user',
                           required=True)

    def add_args_records_limit_offset(self) -> None:
        """
        Add options for records limit and offset
        """
        group = self.get_group(self.GROUP_ODOO)
        group.add_argument('--odoo_record_count',
                           type=int,
                           help='Record count to process per block',
                           required=True)
        group.add_argument('--odoo_record_starting',
                           type=int,
                           default=0,
                           help='Starting record to process',
                           required=False)

    def add_group_options(self) -> argparse._ArgumentGroup:
        """
        Add options group
        """
        return self.add_group(self.GROUP_OPTIONS)

    def raise_error(self, text):
        """
        Raise command line error

        :param text: Text to display
        """
        raise self.parser.error(message=text)
