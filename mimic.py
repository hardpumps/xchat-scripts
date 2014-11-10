#!/usr/bin/python
# -*- coding: utf-8 -*



__module_name__ = "mimic.py"
__module_version__ = "1.0"
__module_description__ = "Mimic another chatter on irc."

import xchat
xchat.prnt(">> " + __module_name__ + " " + __module_version__ + " loaded.")

TARGET_HOST = None
TARGET_CHAN = None

def mimic(word, word_eol, userdata):
    global TARGET_HOST, TARGET_CHAN
    try:
        target_nick = word[1]
        target_chan = word[2]
    except IndexError:
        xchat.prnt("[!] mimic.py Error: Missing target arguments!")
    else:
        ctx = xchat.find_context(channel=target_chan)
        if ctx:
            target_host = [user.host for user in ctx.get_list("users") 
                            if xchat.nickcmp(user.nick, target_nick) != 0]
            if target_host:
                TARGET_HOST = target_host[0]
                TARGET_CHAN = target_chan
            else:
                xchat.prnt("[!] mimic.py Error: Missing host for %s" % target_nick) 
        else:
            xchat.prnt("[!] mimic.py Error: Missing context for %s" % target_chan) 
        return xchat.EAT_ALL
xchat.hook_command("mimic", mimic)

def unmimic(word, word_eol, userdata):
    global TARGET_HOST, TARGET_CHAN
    TARGET_HOST = None
    TARGET_CHAN = None
    xchat.prnt("[!] mimic.py Status: Target information reset!") 
    return xchat.EAT_ALL
xchat.hook_command("unmimic", unmimic)

def on_target_message(word, word_eol, userdata):
    global TARGET_HOST, TARGET_CHAN
    if TARGET_HOST and TARGET_CHAN:
        ctx = xchat.find_context(channel=TARGET_CHAN)
        if ctx:
            nick = word[0]
            host = [user.host for user in ctx.get_list("users") 
                    if xchat.nickcmp(user.nick, nick) != 0]
            if host:
                print host
                print host[0]
                if host[0] == TARGET_HOST:
                    print "MATCH"
                    message = word[1]
                    ctx.command("say %s" % message)
        else:
            xchat.prnt("[!] mimic.py Error: Missing context for %s" % TARGET_CHAN)
    return xchat.EAT_NONE

xchat.hook_print("Channel Message", on_target_message)
xchat.hook_print("Channel Msg Hilight", on_target_message)
xchat.hook_print("Channel Action Hilight", on_target_message)
xchat.hook_print("Channel Action", on_target_message)
