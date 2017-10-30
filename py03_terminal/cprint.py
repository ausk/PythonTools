#!/usr/bin/python3
# https://pypi.python.org/pypi/termcolor
# https://pypi.python.org/pypi/boltons
# https://pypi.python.org/pypi/moleskin

"""
https://media.readthedocs.org/pdf/boltons/latest/boltons.pdf
https://pypi.python.org/pypi/boltons
https://github.com/mahmoud/boltons

https://docs.python.org/3/library/ctypes.html

"""

import sys
from termcolor import colored, cprint

text = colored('Hello, World!', 'red', attrs=['reverse', 'blink'])
print(text)
cprint('Hello, World!', 'green', 'on_red')

print_red_on_cyan = lambda x: cprint(x, 'red', 'on_cyan')
print_red_on_cyan('Hello, World!')
print_red_on_cyan('Hello, Universe!')

for i in range(10):
    cprint(i, 'magenta', end=' ')
print()



cprint("Attention!", 'red', attrs=['bold'], file=sys.stderr)

