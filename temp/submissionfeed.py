# -*- coding: utf-8 -*-
"""
Created on Sat Aug 08 00:35:42 2015

@author: Jamie
"""
TITLE = 'Submission Feed'
VERSION = '0.0.5'
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

def get_new_topics(r, subreddit, seen_new_topics, limit=10):
    new_submissions = r.get_subreddit(subreddit).get_new(limit=limit)
    new_topics = []
    while True:
        try:
            sub = new_submissions.next()
        except StopIteration:
            break
        if sub.id in seen_new_topics:
            continue
        else:
            new_topics.append(sub)
            seen_new_topics.append(sub.id)
    return new_topics

def subreddit_submissions(r, subreddit):
    print Fore.YELLOW
    limit = 100
    
    seen_hot_topics = []
    seen_new_topics = []
    seen_top_topics = []
    
    wait_time = 1
    run = 0
    
    print Fore.RED
    logger.info('Loading subreddits')
    while True:
        ctypes.windll.kernel32.SetConsoleTitleA("Subreddit Feed: Tracking %s" % subreddit)

        #   top topics        
        top_topics = []
        if run == 0:
            #   print top ten posts over all subreddits
            top_topics.extend(get_top_topics(r, subreddit, seen_top_topics, limit=10))
            for topic in top_topics:
                print_submission(topic, title_colour=Fore.GREEN)
                time.sleep(3)
        elif run == 1:
            #   collect top ten posts in each subreddit
            for sub in subreddit.split('+'):
                top_topics.extend(get_top_topics(r, sub, seen_top_topics, limit=10))
            if len(top_topics) == 0:
                wait_time += 1
            else:
                wait_time = 1
        else:
            #   collect and print top ten posts in each subreddit
            for sub in subreddit.split('+'):
                for topic in get_top_topics(r, sub, seen_top_topics, limit=10):
                    print_submission(topic, title_colour=Fore.GREEN)
                    time.sleep(3)
#                top_topics.extend(get_top_topics(r, sub, seen_top_topics, limit=10))
            if len(top_topics) == 0:
                wait_time += 1
            else:
                wait_time = 1
#            for topic in top_topics:
#                print_submission(topic, title_colour=Fore.GREEN)
#                time.sleep(3)
        
        #   hot topics        
        hot_topics = []
        if run == 0:
            #   print hot ten posts over all subreddits
            hot_topics.extend(get_hot_topics(r, subreddit, seen_hot_topics, limit=10))
        elif run == 1:
            #   collect top ten posts in each subreddit
            for sub in subreddit.split('+'):
                hot_topics.extend(get_hot_topics(r, sub, seen_hot_topics, limit=10))
            if len(hot_topics) == 0:
                wait_time += 1
            else:
                wait_time = 1
        else:
            #   collect and print top ten posts in each subreddit
            for sub in subreddit.split('+'):
                hot_topics.extend(get_hot_topics(r, sub, seen_hot_topics, limit=10))
            if len(hot_topics) == 0:
                wait_time += 1
            else:
                wait_time = 1
            for topic in hot_topics:
                print_submission(topic, title_colour=Fore.MAGENTA)
                time.sleep(2)

        new_topics = get_new_topics(r, subreddit, seen_new_topics, limit=100)
        if len(new_topics) == 0:
            wait_time += 1
        else:
            wait_time = 1
        if run != 0 :
            for topic in reversed(new_topics):
                if topic.id not in seen_hot_topics and topic.id not in seen_top_topics:
                    print_submission(topic, title_colour=Fore.CYAN)
                    time.sleep(1)
            
            
    
        run += 1            
        
        if wait_time <= 5:
            ctypes.windll.kernel32.SetConsoleTitleA("Subreddit Feed: waiting")
            time.sleep(wait_time)
        else:
            ctypes.windll.kernel32.SetConsoleTitleA("Subreddit Feed: waiting")
            time.sleep(5)


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
                                      'news', 'worldnews', 'europe', 'uklaw', 'eulaw',
                                      'python', 'technology', 'dota2', 'lifeprotips', 'gallifrey',
                                      'programming', 'teslamotors',
                                      'startrek', 'todayilearned', 'iama', ])
                #subreddit = str(raw_input("Enter subreddit:\t"))             
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
    setup_logging(default_level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    logger.info(''.join([TITLE, ' v', VERSION, ' ', AUTHOR]))
    sys.exit(main(sys.argv))

