# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 23:30:41 2014

@author: Jamie
"""
import sys
from distutils.core import setup
import py2exe
from multifeed import TITLE, VERSION, AUTHOR
import shutil
import os

shutil.rmtree('dist')
sys.argv.append("py2exe")


setup(
        console=['multifeed.py'],
        name = TITLE,
        version = VERSION,
        author= AUTHOR,
        data_files = ["praw.ini", "checklist.txt"],
        zipfile = None, #"{}.zip".format(TITLE),
        options={
                "py2exe":{
                        "unbuffered": True,
                        "bundle_files":1,
                        "optimize": 0,
                        "compressed": True,
                        "xref": False,
                        "ascii": False,
                        "includes":["htmlentitydefs"]
                }
        
        }
        
)
shutil.rmtree('build')
os.remove(os.path.join('dist', 'w9xpopen.exe'))