#!/usr/bin/python
# -*- coding: utf-8 -*-

__module_name__ = "scroll.py"
__module_version__ = "2.0"
__module_description__ = "IRC ascii art scroller/transformer"

import xchat, random, re, os
xchat.prnt(">> " + __module_name__ + " " + __module_version__ + " loaded.")
running = True

def invert(text):
    # 00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 becomes
    # 01 00 08 13 10 11 09 12 02 06 04 05 07 03 15 14
    _text = []
    inv_dict = {
                '00':'01', '01':'00', '02':'08', '03':'13', '04':'10', 
                '05':'11', '06':'09', '07':'12', '08':'02', '09':'06', 
                '10':'4', '11':'5', '12':'7', '13':'3', '14':'15', 
                '15':'14', '0':'1', '1':'0', '2':'8', '3':'13', '4':'10', 
                '5':'11', '6':'9', '7':'12', '8':'2', '9':'6'
    }
    for txt in text:
        for i, j in inv_dict.iteritems():
            txt = txt.replace(i, j)
        _text.append(txt)
    return _text
    
# def fatten(text, n):
#     _text = []
#     shit = []
#     lol = ['1','2','3','4','5','6','7','8','9','0','', ',']
#     n = int(n)
#     for txt in text:
#         for t in txt:
#             if t not in lol:
#                 shit.append(t)
#         shit = set(shit)
#         shit = list(shit)
#         for s in shit:
#             txt = txt.replace(s, s*n)
#         _text.append(txt)
#     return _text

def stack(text, n):
    _text = []
    n = int(n)
    for txt in text:
        for x in xrange(n):
            _text.append(txt)
    return _text 

def begin(text, s):
    _text = []
    for txt in text:
        txt = "%s %s" % (s, txt)
        _text.append(txt)
    return _text

def nicklist(text):
    _text = []
    _nicklist = [user.nick for user in xchat.get_list('users') 
                    if xchat.nickcmp(user.nick, my_nick) != 0]
    longest_nick_len = len(max(_nicklist, key=len))
    for txt in text:
        _nick = random.choice(_nicklist)
        space = longest_nick_len - len(_nick)
        txt = "%s%s %s" % (_nick, " "*(space), txt)
        _text.append(txt)
    return _text

def wavy(text, n):
    _text = []
    inc = True
    x = 0
    for txt in text:
        txt = "%s%s" % (" "*x, txt)
        _text.append(txt)
        if inc:
            x+=1
            if x == int(n):
                inc = False
        else:
            x-=1
            if x == 0:
                inc = True
    return _text

def flip(text):
    _text = reversed([txt for txt in text])
    return _text

def parabola(text, n):
    _text = []
    x, d = 0, 1
    n = int(n)
    _max = (n*n)/4
    for txt in text:
        _offset = (n * x - (x * x)) * d
        txt = ' '*(_max+_offset) + txt
        x += d
        if (x == 0 or x == n):
            d = d * -1
        _text.append(txt)
    return _text

def transform(*args):
    text = args[0]
    if len(args[1].split()) > 1:
        func, param = args[1].split()
        f = funcs[func]
        return f(text, param)
    else:
        func = args[1]
        f = funcs[func]
        return f(text)

def search(path, search_term):
    files = [os.path.join(root, name).replace(path, '').replace('.txt', '') 
                for root, dirs, files in os.walk(path) 
                    for name in files if search_term in name 
                        if name.endswith('txt')]
    if len(files) > 0:
        xchat.prnt("[!] %d files found" % len(files))
        xchat.prnt('\n'.join(files))
    else:
        xchat.prnt("[!] 0 files found")

funcs = {
    'wavy': wavy,
    'flip': flip,
    'para': parabola,
    'begin': begin,
    'stack': stack,
    #'fatten': fatten,
    'invert': invert,
    'nicklist': nicklist
}

def scroll(word, word_eol, userdata):
    global running
    running = True
    path = 'F:\\backup\\ascii\\'
    if len(word) > 2:
        data = word_eol[2]
        if data[1:].split()[0] == 'search':
            search(path, word[1])
            return
    filepath = '%s%s.txt' % (path, word[1])
    try:
        ascii_txt = open(filepath, 'r').readlines()
    except IOError as e:
        xchat.prnt(e)
        return
    speed = 50
    if len(word) > 2:
        if data.split()[0] == '-speed':
            speed = int(data.split()[1])*10
        if data[0] != '-':
            print ">>Improper argument ('/scroll ascii -arg1 -arg2')"
            return
        _args = [arg for arg in data[1:].split(' -') if arg.split()[0] in funcs.keys()]
        for arg in _args:
            ascii_txt = transform(ascii_txt, arg)
    ctx = xchat.get_context()
    def on_timer(userdata):
        for line in ascii_txt:
            if running:
                ctx.command("say %s" % line.rstrip('\n'))
                return ascii_txt.pop(0)
    xchat.hook_timer(speed, on_timer)
    return xchat.EAT_ALL
xchat.hook_command("scroll", scroll, help="/scroll filename [-arg(s)]")

def stop(word, word_eol, data):
    global running
    running = False
    return xchat.EAT_ALL
xchat.hook_command("stop", stop)