#!/usr/bin/env python


import sys
from color import Text



def success_msg(text):
    text = Text(text).color('fg_green')
    print(text)



def info_msg(text):
    text = Text(text).color('fg_blue')
    print(text)



def error_msg(text):
    text = Text('ERROR: ' + text).color('fg_white', 'bg_red')
    print(text, file=sys.stderr)



def main():
    msg('This is normal message')
    error_msg('This is error message')



if __name__ == '__main__':
    main()