"""pytests for StefParse"""

import logging
import os

from stefparse.parse import start_stefparse

BASEDIR = os.path.dirname(os.path.realpath(__file__))


def test_stefparse():
    """Simple test run of stefparse using testlogs.txt as test input"""
    # initialize logging similar to stefparse/__main__
    handlers = list()
    handlers.append(logging.StreamHandler())
    level = logging.DEBUG
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=handlers,
    )

    # open a text file that fakes a serial input
    test_ser = open(os.path.join(BASEDIR, "testlogs.txt"))

    # start stefparse with fake serial input
    start_stefparse(test_ser)


test_stefparse()
