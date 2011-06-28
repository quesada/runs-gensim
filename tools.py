
"""
some functions I need for almost all tasks or runs
"""

from os import path
from sumatra.parameters import build_parameters
import logging
import os
import sys
import gensim


def get_logger(module, fname):
    """set up a logger for a certain module and log to file and stdout

    standard log level is debug
    """
    logger = logging.getLogger(module)
    # remove the NullHandler
    if len(logger.handlers) == 1:
        logger.removeHandler(logger.handlers[0])
    if len(logger.handlers) == 0:
        file_handler = logging.FileHandler(fname, 'w')
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    logger.setLevel(logging.DEBUG)
    return logger

def setup(param_file=None):
    if param_file:
        p = build_parameters(param_file)
        base_path = path.join(path.dirname(__file__), 'test', 'data')
    else:
        p = build_parameters(sys.argv[1])
        base_path = p['base_path']
    output_dir = path.join(base_path,
                              p['result_path'],
                              p['sumatra_label'])
    if not path.exists(output_dir):
        os.mkdir(output_dir)
    return p, base_path, output_dir
