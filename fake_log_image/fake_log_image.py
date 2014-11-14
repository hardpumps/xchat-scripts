#!/usr/bin/python
# -*- coding: utf-8 -*-

__module_name__ = "fake_log_image.py"
__module_version__ = "1.0"
__module_description__ = "Fake log image generator."

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from time import time
from datetime import datetime
import os
import random
import xchat
import pyimgur

xchat.prnt(">> " + __module_name__ + " " + __module_version__ + " loaded.")

SRC_FILENAME = 'image.png'
NEW_FILENAME = 'new.png'
PATH = os.path.dirname(os.path.abspath(__file__))+'/'
UPLOAD_TO_IMGUR = True


def fake_log_image_generator(nicklist, network, chan, my_nick, topic):
    chats = open(PATH+'chats.txt', 'r').read().split('\n')
    chats = [c for c in chats if len(c) > 1]
    img = Image.open(PATH+SRC_FILENAME)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('/usr/share/fonts/truetype/droid/DroidSansMono.ttf', 13)
    font2 = ImageFont.truetype('/usr/share/fonts/truetype/droid/DroidSans-Bold.ttf', 13)
    nicklist = [(nick, random.choice(['red', 'blue', 'green', 'brown', 
                    'purple', 'yellow', 'orange'])) for nick in nicklist]
    timestamp = time()-500
    for i in xrange(26):
        txt = random.choice(chats)
        idx = chats.index(txt)
        chats.pop(idx)
        j = random.choice(nicklist)
        nick = '<'+j[0]+'>'
        timestamp = timestamp + random.randint(20,200)
        ts = '[%s]' % datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')
        y = 90+(i*15)
        x = 196
        nick_length = len(nick)
        if nick_length > 3:
            x = 220-(nick_length*8)
        draw.text((x, y), nick, font=font, fill=j[1])
        draw.text((5, y), ts, font=font)
        draw.text((230, y), txt, font=font)
    title_bar = "HexChat: %s @ %s / %s (+) (%d)" % (my_nick, network, chan, len(nicklist))
    tab_bar = ' %s    %s' % (network, chan)
    draw.text((387, 4), title_bar, font=font2)
    draw.text((5, 63), topic, font=font)
    draw.text((7, 34), tab_bar, font=font, fill="grey")
    img.save(PATH+NEW_FILENAME)      
    
def fake(word, word_eol, userdata):
    my_nick = xchat.get_info('nick')
    try:
        topic = word_eol[1]
    except:
        xchat.prnt("fake_log_image.py Error: Invalid arguments!") #add error func later
    else:
        nicklist = [xchat.strip(user.nick) for user in xchat.get_list('users')]
        network = xchat.get_info('network')
        chan = xchat.get_info('channel')
        fake_log_image_generator(nicklist, network, chan, my_nick, topic)
        if UPLOAD_TO_IMGUR:
            try:
                import pyimgur
            except ImportError:
                xchat.prnt("[!] fake_log_image.py Error: pyimgur module not found!")
            else:
                client_id = ''
                im = pyimgur.Imgur(client_id)
                uploaded_image = im.upload_image(PATH+NEW_FILENAME, title="100 PERCENT AUTHENTIC REAL LOGS")
                lnk = uploaded_image.link
                lnk = lnk.replace('http', 'https')
                xchat.command("say I just took a screenshot of this chat: "+lnk)
    return xchat.EAT_ALL
xchat.hook_command("fake", fake, help="/fake [topic text]")
