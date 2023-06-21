#!/usr/bin/env python

import sys
from color import Text

def start_msg(text):
    text = Text(text).color('fg_bright_cyan')
    print(text)

def success_msg(text):
    text = Text(text).color('fg_green')
    print(text)

def info_msg(text):
    text = Text(text).color('fg_blue')
    print(text)

def error_msg(text):
    text = Text('ERROR: ' + text).color('fg_white', 'bg_red')
    print(text, file=sys.stderr)

def attention_msg(text):
    text = Text(text).color('fg_red', 'bg_yellow')
    print(text)

def end_msg(text):
    text = Text(text).color('fg_bright_cyan')
    print(text)


def main():
    start_msg('This is start message')
    success_msg('This is success message')
    info_msg('This is info message')
    error_msg('This is error message')
    attention_msg('This is attention message')
    end_msg('This is end message')


if __name__ == '__main__':
    main()