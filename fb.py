#!/usr/bin/python
# -*- coding: utf-8 -*-

__module_name__ = "fb.py"
__module_version__ = "2.0"
__module_description__ = "Flashing bar/mass highlight script."

import xchat, random
xchat.prnt(">> " + __module_name__ + " " + __module_version__ + " loaded.")
my_nick = xchat.get_info('nick')

def error(msg):
    xchat.prnt("4[!] %s Error: %s" % (__module_name__, msg))
    
def color():
    color_range = range(2, 16)
    fg = random.choice(color_range)
    color_range.remove(fg)
    bg = random.choice(color_range)
    return '%s,%s' % (fg, bg)

def fb(word, word_eol, userdata):
    nicklist = [user.nick for user in xchat.get_list('users') 
                if xchat.nickcmp(user.nick, my_nick) != 0]
    if len(nicklist) < 1:
        error("No users in channel!")
    else:
        try:
            mode = word[1]
            if not mode in '1 2 3 4 5':
                error("Invalid mode argument!")
        except IndexError:
            error("Missing mode argument! (e.g. /fb 1, 2, 3, 4, or 5)")
        else:
            if mode in '1 2 3 4':
                if mode == '1':
                    if len(word) < 4 or not '$n' in word_eol:
                        error("Not enough arguments!")
                    else:
                        cmd = word[2]
                        message = word_eol[3]
                        for nick in nicklist:
                            xchat.command("%s %s" % (cmd, message.replace('$n', nick)))
                elif mode in '2 3 4':
                    if len(word) < 3:
                        error("Not enough arguments!")
                    else:
                        message = word_eol[2]
                        if mode == '2':
                            message = ' '.join([nick+' '+message for nick in nicklist])
                            xchat.command("say %s" % message)
                        else:
                            placeholder = []
                            for nick in nicklist:
                                usr_code = color()
                                msg_code = color()
                                placeholder.append("%s%s%s %s" % (usr_code, nick, msg_code, message))
                            if mode == '3':
                                for line in placeholder:
                                    xchat.command("say %s" % line)
                            else:
                                message = ''.join(placeholder)
                                xchat.command("say %s" % message)
            else:
                x = True
                for nick in nicklist:
                    if x:
                        message = "01,08/!\08,01* *FLASHING BAR* *01,08/!\\"
                        x = False
                    else:
                        message = "08,01/!\01,08* *FLASHING BAR* *08,01/!\\"
                        x = True
                    space = 65 - (len(message) + len(nick))
                    new_msg = "%s %s> %s" % (nick, "-"*(space-1), message)
                    xchat.command("say %s" % new_msg)
    return xchat.EAT_ALL
xchat.hook_command("fb", fb, help="/fb [1,2 [$n is replaced with the user nick], 3, 4, 5]")
