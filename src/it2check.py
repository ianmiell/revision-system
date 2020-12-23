# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import sys
import termios


def csi(num):
    """
    Control Sequence Introducer
    https://en.wikipedia.org/wiki/ANSI_escape_code#CSI_sequences
    """
    print('\x1b[{}n'.format(num), end='')
    sys.stdout.flush()


def read_dsr():
    """
    Read device status report response
    """
    # discard leading '\x1b['
    sys.stdin.read(2)

    dsr = ''
    while True:
        byte = sys.stdin.read(1)
        if byte == 'n':
            break
        dsr += byte
    return dsr


def check():
    """
    Translated to Python from https://iterm2.com/utilities/it2check
    """
    if not sys.stdin.isatty() or not sys.stdout.isatty():
        return False

    stdin_fd = sys.stdin.fileno()
    stdin_old_attr = termios.tcgetattr(stdin_fd)
    try:
        # Turn off echo so the terminal and I can chat quietly.
        # As described in https://docs.python.org/2/library/termios.html#example
        stdin_new_attr = termios.tcgetattr(stdin_fd)
        stdin_new_attr[3] &= ~termios.ECHO & ~termios.ICANON
        termios.tcsetattr(stdin_fd, termios.TCSADRAIN, stdin_new_attr)

        # Send iTerm2-proprietary code. Other terminals ought to ignore it (but are
        # free to use it respectfully).  The response won't start with a 0 so we can
        # distinguish it from the response to DSR 5. It should contain the terminal's
        # name followed by a space followed by its version number and be terminated
        # with an n.
        csi(1337)

        # Report device status. Responds with esc [ 0 n. All terminals support this. We
        # do this because if the terminal will not respond to iTerm2's custom escape
        # sequence, we can still read from stdin without blocking indefinitely.
        csi(5)

        version_string = read_dsr()
        if version_string not in {'0', '3'}:
            # Already read DSR 1337. Read DSR 5 and throw it away.
            read_dsr()
        return version_string.startswith('ITERM2 ')
    except Exception:
        return False
    finally:
        termios.tcsetattr(stdin_fd, termios.TCSADRAIN, stdin_old_attr)
