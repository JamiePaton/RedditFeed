# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 19:35:53 2015

@author: Jamie
"""
TITLE = 'Reddit Comment Tracking'
VERSION = '0.4.3'
AUTHOR = 'Jamie Paton'

from colorama import Fore, Back
import HTMLParser

replace_dict = {'&lt;': '<', '&gt;': '>'}

def multiple_replace(text, wordDict=replace_dict):
    newtext = ""
    for char in text:
        try:
            newtext += wordDict[char]
        except KeyError:
            newtext += char
    return newtext


def print_char(char, colour=Fore.WHITE, delay=0.05, lead=True):
    try:
        if char == '\n':
            print '\n'
#        elif char == u'\xa3':
#            print u'£',
        elif char in ['.', '!', '?']:
            if lead:
                print "\b{}".format(Fore.YELLOW + "_"),
                sleep(10*delay)
                print "\b\b{}".format(colour + char),
                sleep(5*delay)
            else:
                print "\b{}".format(colour + char),
                sleep(15*delay)
        elif char in [' ']:
            print "\b{}".format(Back.BLACK + " "),
        else:
            if lead:
                print "{}".format(Fore.RED + ">"),
                sleep(0.4*delay)
                print "\b\b{}".format(Fore.YELLOW + "_"),
                sleep(0.2*delay)
                print "\b\b\b{}".format(colour + char),
                sleep(0.1*delay)
            else:
                print "\b{}".format(colour + char),
                sleep(0.1*delay)
    except (RedirectException, UnicodeEncodeError):
        logger.exception(Fore.MAGENTA+"\nERROR")


def print_line(line, colour=Fore.WHITE, delay=0.05, lead=True):
    char_list = list(line)
    for char in char_list:
        print_char(char, colour, delay, lead)
    print "\b \b"
#    print line

def subreddit_comments(r, subreddit):
    print Fore.YELLOW
    limit = 10
    print_limit = 10
    comments = praw.helpers.comment_stream(r, subreddit, limit=limit, verbosity=0)
    seen_submissions = []
    init_count = 0
    while True:
        first_seen = False
        comment = comments.next()
        if comment.submission.id not in seen_submissions:
            seen_submissions.append(comment.submission.id)
            first_seen = True

        if init_count < limit and init_count < limit-print_limit:
            init_count += 1
            for line in textwrap.wrap(str(init_count) + ":\t"+ comment.submission.title, 77):
                print_line(line, colour=Fore.MAGENTA, delay=0.001, lead=False)
            continue
        
        elif init_count >= limit-print_limit:
            init_count += 1
            print
            date = "{0:>78}".format(
                datetime.datetime.fromtimestamp(
                comment.created_utc).strftime("%I:%M:%S %p %A, %d %B %Y"))
            title = comment.submission.title
            print_line(date, colour=Fore.WHITE, delay=0.01, lead=False)
            print_line("{0:>78}".format(str(comment.submission.subreddit)),
                       colour=Fore.YELLOW, delay=0.01, lead=False)
                   
            for line in textwrap.wrap(title, 77):
                print_line(line, colour=Fore.MAGENTA, delay=0.02)
        
        if first_seen:
            try:
#                print_line("{0:>76}".format(str(comment.submission.author) + 
#                    " ("+str(comment.submission.author.link_karma) + "|" +
#                    str(comment.submission.author.comment_karma) + ')'), 
#                    colour=Back.BLUE+Fore.RED, delay=0.01)
#                print Back.BLACK,
                for line in comment.submission.selftext.split('\n'):
                    for subline in textwrap.wrap(line, 77):
                        print_line(subline, colour=Fore.CYAN, delay=0.01)
            except AttributeError:
                pass

#        print_line(str(comment.author) + " ("+str(comment.author.link_karma) + "|" +\
#            str(comment.author.comment_karma) + '):', colour=Fore.RED, delay=0.01)
#        sleep(random.random())
        
        for line in comment.body.split('\n'):
            for subline in textwrap.wrap(line, 77):
                print_line(subline, colour=Fore.GREEN, delay=0.008)
#        sleep(random.random())


def main(args):
    from colorama import init
    init()
    r = praw.Reddit('comment parser')
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
                subreddit = 'unitedkingdom+ukpolitics+london+news'
                #subreddit = str(raw_input("Enter subreddit:\t"))             
            title = "Reddit Comment Tracking: %s" % subreddit
            ctypes.windll.kernel32.SetConsoleTitleA(title)
            subreddit_comments(r, subreddit)
        except KeyboardInterrupt:
            ctypes.windll.kernel32.SetConsoleTitleA(TITLE)
            print Fore.YELLOW
        except HTTPError:
            logger.exception(Fore.MAGENTA+"\nERROR")
            sleep(5)
            continue


if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info(''.join([TITLE, ' v', VERSION, ' ', AUTHOR]))
    import consolefont
    consolefont.main()
    import ctypes
    ctypes.windll.kernel32.SetConsoleTitleA(TITLE)
    import sys
    from time import sleep
    import random
    import datetime
    import textwrap
    import praw
    from praw.internal import RedirectException
    sys.exit(main(sys.argv))
