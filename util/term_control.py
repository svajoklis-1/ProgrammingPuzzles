'''
	Further reading
	https://ss64.com/nt/syntax-ansi.html
	https://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html
'''


import os
from enum import Enum


class TermColor(Enum):
    BLACK = 0
    MAROON = 1
    GREEN = 2
    OLIVE = 3
    NAVY = 4
    PURPLE = 5
    TEAL = 6
    GRAY = 7
    SILVER = 8
    RED = 9
    LIME = 10
    YELLOW = 11
    BLUE = 12
    FUSCHIA = 13
    AQUA = 14
    WHITE = 15


ForegroundColorMap = {
    TermColor.BLACK: '[30m',
    TermColor.MAROON: '[31m',
    TermColor.GREEN: '[32m',
    TermColor.OLIVE: '[33m',
    TermColor.NAVY: '[34m',
    TermColor.PURPLE: '[35m',
    TermColor.TEAL: '[36m',
    TermColor.GRAY: '[37m',
    TermColor.SILVER: '[30;1m',
    TermColor.RED: '[31;1m',
    TermColor.LIME: '[32;1m',
    TermColor.YELLOW: '[33;1m',
    TermColor.BLUE: '[34;1m',
    TermColor.FUSCHIA: '[35;1m',
    TermColor.AQUA: '[36;1m',
    TermColor.WHITE: '[37;1m'
}


BackgroundColorMap = {
    TermColor.BLACK: '[40m',
    TermColor.MAROON: '[41m',
    TermColor.GREEN: '[42m',
    TermColor.OLIVE: '[43m',
    TermColor.NAVY: '[44m',
    TermColor.PURPLE: '[45m',
    TermColor.TEAL: '[46m',
    TermColor.GRAY: '[47m',
    TermColor.SILVER: '[40;1m',
    TermColor.RED: '[41;1m',
    TermColor.LIME: '[42;1m',
    TermColor.YELLOW: '[43;1m',
    TermColor.BLUE: '[44;1m',
    TermColor.FUSCHIA: '[45;1m',
    TermColor.AQUA: '[46;1m',
    TermColor.WHITE: '[47;1m'
}


RESET = '[0m'
ESC = chr(27)


class TermControl:
    @staticmethod
    def clear():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def control(control_string):
        print(ESC + control_string, end='')

    @staticmethod
    def set_foreground(color: TermColor):
        print(ESC + ForegroundColorMap[color], end='')

    @staticmethod
    def set_background(color: TermColor):
        print(ESC + BackgroundColorMap[color], end='')

    @staticmethod
    def reset_color():
        print(ESC + RESET, end='')

    @staticmethod
    def move_cursor_up(amount: int):
        print(ESC + f'[{amount}A', end='')

    @staticmethod
    def move_cursor_down(amount: int):
        print(ESC + f'[{amount}B', end='')

    @staticmethod
    def move_cursor_right(amount: int):
        print(ESC + f'[{amount}C', end='')

    @staticmethod
    def move_cursor_left(amount: int):
        print(ESC + f'[{amount}D', end='')
