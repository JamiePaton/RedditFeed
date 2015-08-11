# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 18:56:07 2015

@author: Jamie
"""
TITLE = 'console'
VERSION = '0.0.1'
AUTHOR = 'Jamie Paton'

import sys
import logging
from colorama import Fore


def multiple_replace(text, wordDict=replace_dict):
    newtext = ""
    for char in text:
        try:
            newtext += wordDict[char]
        except KeyError:
            newtext += char
    return newtext

def print_char(char, colour=Fore.WHITE, delay=0.05, lead=True):
    """
    PROCEDURE:  Prints a character to the console
    
    Parameters
    ----------
    char :      str
                    character to be printed
    colour :    int, optional
                    colour code
    delay :     float, optional
                    delay time between character printing
    lead :      bool, optional
                    print loading characters first
    Raises
    ----------
    UnicodeEncodeError
                if there is a unicode error
    
    """
    try:
        if char == '\n':
            print '\n'
        elif char == u'\xa3':
            print u'£',
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
    except (UnicodeEncodeError):
        logger.exception()

def main(args):
    
    return None
    

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info(''.join([TITLE, ' v', VERSION, ' ', AUTHOR]))
    sys.exit(main(sys.argv))

