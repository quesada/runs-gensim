
"""
some functions I need for almost all tasks or runs
"""

import logging

def get_logger(module, fname):
    """set up a logger for a certain module and log to file and stdout

    standard log level is debug
    """
    logger = logging.getLogger(module)
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
