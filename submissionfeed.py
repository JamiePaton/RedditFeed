# -*- coding: utf-8 -*-
"""
Created on Sat Aug 08 00:35:42 2015

@author: Jamie
"""
TITLE = 'Submission Feed'
VERSION = '0.0.1'
AUTHOR = 'Jamie E Paton'
TEST = 0

import sys
import logging
import logging.config
import unittest
#import hypothesis as hs
import praw
from colorama import Fore, Back
import ctypes
import datetime
import time
import textwrap

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

def print_char(char, colour=Fore.WHITE, delay=0.05, lead=True):
    try:
        if char == '\n':
            print '\n'
#        elif char == u'\xa3':
#            print u'£',
        elif char in ['.', '!', '?']:
            if lead:
                print "\b{}".format(Fore.YELLOW + "_"),
                time.sleep(10*delay)
                print "\b\b{}".format(colour + char),
                time.sleep(5*delay)
            else:
                print "\b{}".format(colour + char),
                time.sleep(15*delay)
        elif char in [' ']:
            print "\b{}".format(Back.BLACK + " "),
        else:
            if lead:
                print "{}".format(Fore.RED + ">"),
                time.sleep(0.4*delay)
                print "\b\b{}".format(Fore.YELLOW + "_"),
                time.sleep(0.2*delay)
                print "\b\b\b{}".format(colour + char),
                time.sleep(0.1*delay)
            else:
                print "\b{}".format(colour + char),
                time.sleep(0.1*delay)
    except (praw.internal.RedirectException, UnicodeEncodeError):
        logger.exception(Fore.MAGENTA+"\nERROR")


def print_line(line, colour=Fore.WHITE, delay=0.05, lead=True):
    char_list = list(line.replace(u"\u2018", "'").replace(u"\u2019", "'"))
    for char in char_list:
        print_char(char, colour, delay, lead)
    print "\b \b"

def subreddit_submissions(r, subreddit):
    print Fore.YELLOW
    limit = 2
    
    hot_submissions = r.get_subreddit(subreddit).get_hot(limit=limit)
    print Fore.RED
    logger.info('Displaying hot topics')
    

    seen_submissions = []
    while True:
        time.sleep(1)
        try:
            submission = hot_submissions.next()
        except StopIteration:
            break
        date = "{0:>78}".format(
                datetime.datetime.fromtimestamp(
                submission.created_utc).strftime("%I:%M:%S %p %A, %d %B %Y"))
        sub = submission.subreddit
        title = submission.title

        print 
        print_line(date, colour=Fore.WHITE, delay=0.01, lead=False)
        print_line("{0:>78}".format(str(sub)),
                       colour=Fore.YELLOW, delay=0.01, lead=False)
        for line in textwrap.wrap(title, 77):
            print_line(line, colour=Fore.MAGENTA, delay=0.01)    
    
    print Fore.RED
    logger.info('Displaying new topics')
    submissions = praw.helpers.submission_stream(r, subreddit, limit=limit, verbosity=0)
    while True:
        time.sleep(1)
        submission = submissions.next()
        date = "{0:>78}".format(
                datetime.datetime.fromtimestamp(
                submission.created_utc).strftime("%I:%M:%S %p %A, %d %B %Y"))
        title = submission.title
        sub = submission.subreddit

        print 
        print_line(date, colour=Fore.WHITE, delay=0.01, lead=False)
        print_line("{0:>78}".format(str(sub)),
                       colour=Fore.YELLOW, delay=0.01, lead=False)
        for line in textwrap.wrap(title, 77):
            print_line(line, colour=Fore.CYAN, delay=0.01)

def main(args):
    from colorama import init
    init()
    import consolefont
    consolefont.main()
    r = praw.Reddit('submission stream')
    r.config.decode_html_entities = True
    r.config.log_requests = 0
    from requests.exceptions import HTTPError
    while True:
        try:
            r = praw.Reddit('comment parser')
            r.config.decode_html_entities = True
            r.config.log_requests = 0
            print Fore.YELLOW
            try:
                subreddit = args[1]
            except IndexError:
                subreddit = '+'.join(['physics', 'science', 'windows',
                                      'uknews', 'unitedkingdom', 'ukpolitics', 'london',
                                      'python', 'technology'])
                #subreddit = str(raw_input("Enter subreddit:\t"))             
            title = "Reddit Comment Tracking: %s" % subreddit
            ctypes.windll.kernel32.SetConsoleTitleA(title)
            subreddit_submissions(r, subreddit)
        except KeyboardInterrupt:
            ctypes.windll.kernel32.SetConsoleTitleA(TITLE)
            print Fore.YELLOW
        except HTTPError:
            logger.exception(Fore.MAGENTA+"\nERROR")
            sleep(5)
            continue
    
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

