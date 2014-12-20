#!/usr/bin/python
from sympy.core.symbol import Dummy
from sympy.utilities.lambdify import lambdify
from sympy import symbols
import sympy
import xchat
import random


__module_name__ = "textplot.py"
__module_version__ = "0.666"
__module_description__ = "Plot crude ascii graphs"


print(">>%s loaded" % __module_name__)


def textplot_(expr, a, b, W=55, H=18):
    """
    Modified version of sympy.plotting.textplot function to allow saving ascii
    plots instead of just printing them.  Also removes the grid and graph
    information because I don't use that lol.
    """
    _text = []

    free = expr.free_symbols
    if len(free) > 1:
        raise ValueError("length can not be greater than 1")
    x = free.pop() if free else Dummy()
    f = lambdify([x], expr)
    a = float(a)
    b = float(b)

    # Calculate function values
    y = [0] * W
    for x in range(W):
        try:
            y[x] = f(a + (b - a)/float(W)*x)
        except (TypeError, ValueError):
            y[x] = 0

    # Normalize height to screen space
    ma = max(y)
    mi = min(y)
    if ma == mi:
        if ma:
            mi, ma = sorted([0, 2*ma])
        else:
            mi, ma = -1, 1
    for x in range(W):
        y[x] = int(float(H)*(y[x] - mi)/(ma - mi))
    margin = 7
    print

    for h in range(H - 1, -1, -1):
        s = [' '] * W
        for x in range(W):
            if y[x] == h:
                if (x == 0 or y[x - 1] == h - 1) and (x == W - 1 or y[x + 1] == h + 1):
                    s[x] = '$h'
                elif (x == 0 or y[x - 1] == h + 1) and (x == W - 1 or y[x + 1] == h - 1):
                    s[x] = '$h'
                else:
                    s[x] = '$h'
        s = "".join(s)
        _text.append(s)
    return _text


def plot(word, word_eol, userdata):
    x = symbols('x')
    arg1 = word[1]
    arg2 = word[2]
    txt = word[3]
    # nicklist = [user.nick for user in xchat.get_list('users') 
    #             if xchat.nickcmp(user.nick, 'erm') != 0]
    # for z in xrange(40):
    #     text = textplot_(sympy.sin(x), z, 5)
    text = textplot_(sympy.sin(x), arg1, arg2)
    text = [i.replace('$h', color(txt)) for i in text]
    for i in text:
        xchat.command("say %s" % i)
    return xchat.EAT_ALL

xchat.hook_command('plot', plot, help="/plot")


def color(txt):
    return "%d,%d%s" % (random.randint(1,10), random.randint(1,10), txt)
