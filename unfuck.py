#!/usr/bin/python

__module_name__ = "unfuck.py"
__module_version__ = "1.0"
__module_description__ = "Counter mass forcejoins by emo opers."

import xchat
xchat.prnt(">> " + __module_name__ + " " + __module_version__ + " loaded.")

SAFE_CHANS = []

def unfuck(word, word_eol, userdata):
    try:
        _chan = word[1]
    except IndexError:
        xchat.prnt("[!] unfuck.py Error: Missing chan argument!")
    else:
        if _chan not in SAFE_CHANS:
            network = xchat.get_info('network')
            chan = [ch for ch in xchat.get_list('channels') if
                ch.channel == _chan][0]
            if chan.network == network and chan.type == 2:
                chan.context.command('timer 3 close') 
xchat.hook_print('You Join', unfuck)

def add_safe_chan(word, word_eol, userdata):
    try:
        chan = word[1]
    except IndexError:
        xchat.prnt("[!] unfuck.py Error: Missing argument!")
    else:
        SAFE_CHANS.append(chan)
xchat.hook_command("safechan", add_safe_chan)
   