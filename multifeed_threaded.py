# -*- coding: utf-8 -*-
"""
Created on Sat Aug 08 14:32:46 2015

@author: Jamie
"""
TITLE = 'Submission Multi Feed'
VERSION = '0.0.2'
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
import Queue

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

def print_submission(submission, title_colour=Fore.CYAN):
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
        print_line(line, colour=title_colour, delay=0.01)

def get_hot_topics(r, subreddit, seen_hot_topics, limit=10):
    hot_submissions = r.get_subreddit(subreddit).get_hot(limit=limit)
    new_hot_topics = []
    while True:
        try:
            sub = hot_submissions.next()
        except StopIteration:
            break
        if sub.id in seen_hot_topics:
            continue
        else:
            new_hot_topics.append(sub)
            seen_hot_topics.append(sub.id)
    return new_hot_topics

def get_top_topics(r, subreddit, seen_top_topics, limit=10):
    top_submissions = r.get_subreddit(subreddit).get_top(limit=limit)
    new_top_topics = []
    while True:
        try:
            sub = top_submissions.next()
        except StopIteration:
            break
        if sub.id in seen_top_topics:
            continue
        else:
            new_top_topics.append(sub)
            seen_top_topics.append(sub.id)
    return new_top_topics

def get_new_topics(r, subreddit, seen_new_topics, queue, limit=10):
    new_submissions = r.get_subreddit(subreddit).get_new(limit=limit)
    while True:
        try:
            sub = new_submissions.next()
        except StopIteration:
            break
        if sub.id in seen_new_topics:
            continue
        else:
            queue.put(sub)
            queue.task_done()
            seen_new_topics.append(sub.id)


def get_submissions(r, subreddit, queue, seen, run, limit=10, ranked='top'):
    for subred in subreddit.split('+'):
        ctypes.windll.kernel32.SetConsoleTitleA("{} v{} {} {}Tracking {} topics in {}".format(TITLE, VERSION, AUTHOR, ' ' * 10, ranked, subred))
        if ranked == 'top':
            submissions = r.get_subreddit(subred).get_top(limit=limit)
        elif ranked == 'hot':
            submissions = r.get_subreddit(subred).get_hot(limit=limit)
        elif ranked == 'new':
            submissions = r.get_subreddit(subred).get_new(limit=limit)
        else: 
            pass
    
        new_seen = []
        _new = []
        while True:
            try:
                sub = submissions.next()
            except StopIteration:
                break
            new_seen.append(sub.id)
            if sub.id in seen[subred][ranked] or run == 1:
                pass
            else:
                if ranked == 'new':
                    _new.append(sub)
                else:
                    queue.put(sub)
                    queue.task_done()
        if ranked == 'new':
            for s in reversed(_new):
                queue.put(s)
                queue.task_done()
        seen[subred][ranked] = new_seen
    ctypes.windll.kernel32.SetConsoleTitleA("{} v{} {}".format(TITLE, VERSION, AUTHOR))


def print_feed(top, hot, new):
    while True:
        while True:
            try:
                print_submission(top.get(timeout=0.1), title_colour=Fore.GREEN)
                time.sleep(2)
            except Queue.Empty:
                break
        try:
            print_submission(hot.get(timeout=0.1), title_colour=Fore.MAGENTA)
            time.sleep(1.5)
            continue
        except Queue.Empty:
            pass
        try:
            print_submission(new.get(timeout=0.1), title_colour=Fore.CYAN)
            time.sleep(1)
            continue
        except Queue.Empty:
            time.sleep(1)
            break

def subreddit_submissions(r, subreddit):
    top_queue = Queue.Queue()
    hot_queue = Queue.Queue()
    new_queue = Queue.Queue()
    
    ranks = ['top', 'hot', 'new']
    seen = {}
    for sub in subreddit.split('+'):
        seen[sub] = {rank: [] for rank in ranks}
    
    run = 0
    while True:
        get_submissions(r, subreddit, top_queue, seen, run, limit=10, ranked='top')
        get_submissions(r, subreddit, hot_queue, seen, run, limit=10, ranked='hot')
        get_submissions(r, subreddit, new_queue, seen, run, limit=100, ranked='new')

        if run >= 1:
            print_feed(top_queue, hot_queue, new_queue)
        run += 1
        time.sleep(5)
    return None


def main(args):
    from colorama import init
    init()
#    import consolefont
#    consolefont.main()
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
                subreddit = '+'.join(['physics', 'science', 'windows', 'economics',
                                      'uknews', 'unitedkingdom', 'ukpolitics', 'london',
                                      'news', 'worldnews', 'europe', 'uklaw', 
                                      'python', 'technology', 'dota2', 'lifeprotips', 'gallifrey',
                                      'programming', 'teslamotors',
                                      #'startrek', 'todayilearned', 'iama', 'eulaw',
                                      ])
                #subreddit = str(raw_input("Enter subreddit:\t"))
#                subreddit = 'dota2'
            title = "Reddit Comment Tracking: %s" % subreddit
            ctypes.windll.kernel32.SetConsoleTitleA(title)
            subreddit_submissions(r, subreddit)
        except KeyboardInterrupt:
            ctypes.windll.kernel32.SetConsoleTitleA(TITLE)
            print Fore.YELLOW
            break
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
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info(''.join([TITLE, ' v', VERSION, ' ', AUTHOR]))
    sys.exit(main(sys.argv))

