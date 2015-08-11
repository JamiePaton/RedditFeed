#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This is an example how to change the font of the windows console.

from http://www.janthor.com/sketches/index.php?/archives/19-How-to-change-the-font-of-the-Windows-console-with-Python.html
"""

from __future__ import print_function, unicode_literals
import ctypes

__author__ = "Jan Thor"
__date__ = "2012-12-17"

LF_FACESIZE = 32
STD_OUTPUT_HANDLE = -11
FALSE = ctypes.c_long(False)
k32 = ctypes.windll.kernel32

class COORD(ctypes.Structure):
    _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]

class CONSOLE_FONT_INFOEX(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.c_ulong),
                ("nFont", ctypes.c_ulong),
                ("dwFontSize", COORD),
                ("FontFamily", ctypes.c_uint),
                ("FontWeight", ctypes.c_uint),
                ("FaceName", ctypes.c_wchar * LF_FACESIZE)]
    
    def __str__(self):
        return ("Font({0.nFont}, {0.dwFontSize.X}, {0.dwFontSize.Y},"
                " {0.FontFamily}, {0.FontWeight}, \"{0.FaceName}\")"
               ).format(self)

SIZEOF_CONSOLE_FONT_INFOEX = ctypes.sizeof(CONSOLE_FONT_INFOEX)

def Font(number, width, height, family, weight, name):
    struct = CONSOLE_FONT_INFOEX()
    struct.cbSize = SIZEOF_CONSOLE_FONT_INFOEX
    struct.nFont = number
    struct.dwFontSize.X = width
    struct.dwFontSize.Y = height
    struct.FontFamily = family
    struct.FontWeight = weight
    struct.FaceName = name
    return struct

TERMINAL = Font(9, 10, 18, 48, 400, "Terminal")
CONSOLAS = Font(9, 8, 32, 54, 400, "Consolas")
LUCIDA = Font(12, 11, 18, 54, 400, "Lucida Console")
LUCIDA14 = Font(12, 8, 14, 54, 400, "Lucida Console")

def setFont(font):
    h = k32.GetStdHandle(STD_OUTPUT_HANDLE)
    if not k32.SetCurrentConsoleFontEx(h, FALSE, ctypes.pointer(font)):
        raise Exception("Unable to set console font.")

def getFont():
    h = k32.GetStdHandle(STD_OUTPUT_HANDLE)
    struct = CONSOLE_FONT_INFOEX()
    struct.cbSize = SIZEOF_CONSOLE_FONT_INFOEX
    if not k32.GetCurrentConsoleFontEx(h, FALSE, ctypes.pointer(struct)):
        raise Exception("Unable to retrieve console font.")
    return struct

# =====================================================================

# The remainder of this module tests if the above is working.
    
# Tested with Python 2.7 on Win32 and Python 3.3 on Win64.

def main():
    import sys
    try:
        import win32gui
    except ImportError:
        win32missing = True
    else:
        win32missing = False
    
    # Unfortunately, prior to Python 3.3, writing to the windows
    # console was quite buggy. To test our new font, I brutally
    # replace the builtin stdout with windows calls. The following
    # class provides a barebone version of such a replacement.
    class Console(object):
        
        def __init__(self):
            self.stdout = k32.GetStdHandle(STD_OUTPUT_HANDLE)
        
        def write(self, text):
            remaining = len(text)
            while remaining > 0:
                n = ctypes.c_ulong(0)
                retval = k32.WriteConsoleW(self.stdout, text, 
                                           min(remaining, 10000), 
                                           ctypes.byref(n), None)
                remaining -= n.value
                text = text[n.value:]
    
    # Enumeration of font family names, to see which fonts we can
    # actually use.
    # I could replace win32gui with ctypes calls, but I’m too lazy.
    if not win32missing:
         def enum_fonts(typeface=None):
            hwnd = win32gui.GetDesktopWindow()
            dc = win32gui.GetWindowDC(hwnd)
            res = []
            def callback(*args):
                res.append(args[0].lfFaceName)
                return 1
            win32gui.EnumFontFamilies(dc, typeface, callback)
            win32gui.ReleaseDC(hwnd, dc)
            return res
    
    # Check if Consolas is available
    if not win32missing and "Consolas" in enum_fonts():
        newfont = CONSOLAS
        testtext = "Ħĕļłǭ Ŵőȑȴḏ"
    else:
        newfont = LUCIDA14
        testtext = "Hĕllō Wőrld"
    
    # Get information about the current font:
    try:
        f = getFont()
        #print("Old:", f)
    except Exception:
        pass
    
    # Attempt to set the new font.
    try:
        setFont(newfont)
        #print("New:", getFont())
    except Exception:
        print("Unable to set console font. Is this running inside an IDE?")
        success = False
    else:
        success = True
    
    # If it seems likely that we are indeed on the
    # windows console, replace it.
    if success:
        console = Console()
    else:
        console = sys.stdout
        
    # Print a test string.
    #print(testtext, file=console)

if __name__ == "__main__":
    main()
    #raw_input()