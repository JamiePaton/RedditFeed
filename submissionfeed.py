# -*- coding: utf-8 -*-
"""
Created on Sat Aug 08 00:35:42 2015

@author: Jamie
"""
TITLE = ''
VERSION = '0.0.0'
AUTHOR = 'Jamie E Paton'
TEST = 0

import sys
import logging
import logging.config
import unittest
#import hypothesis as hs
import praw


def setup_logging(default_path='logs/loggingconfig.json', default_level=logging.INFO,
                  env_key='LOG_CFG'):
    """Setup logging configuration

    """
    import os
    import json
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)

def imports():
    import types
    for name, val in globals().items():
        if isinstance(val, types.ModuleType):
            yield val.__name__


def main(args):
    logger.info('none')
    return None
    
class Testing(unittest.TestCase):
    """
    
    Methods
    -------
    
    
    Notes
    -----
    @given(parameter=hs.strategies.integers())
    
    def test_something(parameter):
        assert type(parameter) == int
    """


if __name__ == '__main__':
    setup_logging(default_level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    logger.info(''.join([TITLE, ' v', VERSION, ' ', AUTHOR]))
    sys.exit(main(sys.argv))

