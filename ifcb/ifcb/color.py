#!/usr/bin/env python


from colorama import just_fix_windows_console
import json



class Text:
    def __init__(self, text):
        just_fix_windows_console()
        self._text = text
        with open('ansi_colors.json', 'r') as f:
            self._colors = json.load(f)

    def color(self, fg_color = 'fg_default', bg_color = 'bg_default', bright = True):
        full_text = f'\033[{self._colors[fg_color]};{self._colors[bg_color]}m{self._text}'
        if bright:
            full_text = f'\033[1;{self._colors[fg_color]};{self._colors[bg_color]}m{self._text}'
        # Reset all attributes at the end
        return full_text+'\033[0m'



if __name__ == '__main__':
    test = Text('Test text')
    print(test.color('fg_yellow', 'bg_black', True))
    print(test.color('fg_yellow', 'bg_black', False))
    print(test.color('fg_magenta', 'bg_bright_green', True))
    print(test.color('fg_magenta', 'bg_bright_green', False))