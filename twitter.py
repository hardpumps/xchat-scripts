#!/usr/bin/python
# -*- coding: utf-8 -*-

__module_name__ = "twitter.py"
__module_version__ = "1.0"
__module_description__ = "Twitter script."

import xchat, tweepy
xchat.prnt(">> " + __module_name__ + " " + __module_version__ + " loaded.")


CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_KEY = ''
ACCESS_SECRET = ''

TWITTER_TAB = '*twitter'
QUIET = False
USER_NAME = 'ermff'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

def twitter_context():
    ctx = xchat.find_context(channel=TWITTER_TAB)
    if not ctx:
        xchat.command('newserver -noconnect "%s"' % TWITTER_TAB)
        ctx = xchat.find_context(channel=TWITTER_TAB)
    return ctx

def timeline(word, word_eol, userdata):
    try:
        user = word[1]
        count = int(word[2])
    except IndexError:
        xchat.prnt("[!] twitter.py Error: Invalid arguments!")
    else:
        tweets = [t.text.encode('utf-8') 
                    for t in api.user_timeline(user, count=count)]
        if tweets:
            ctx = twitter_context()
            for t in tweets:
                ctx.prnt(t)
        else:
            ctx.prnt('[!] twitter.py Error: No tweets found!')
    return xchat.EAT_ALL
xchat.hook_command("timeline", timeline, help="/timline [user_name] [count]")

def tweet(word, word_eol, userdata):
    try:
        tweet_msg = word_eol[1]
    except IndexError:
        xchat.prnt("[!] twitter.py Error: Invalid arguments!")
    else:
        if (len(tweet_msg) > 140):
            xchat.prnt("[!] twitter.py Error: Tweet greater than 140 characters!")
        else:
            api.update_status(tweet_msg)
            if not QUIET:
                status = next(tweepy.Cursor(api.user_timeline).items(), None)
                url = 'https://twitter.com/ermff/status/'+status.id_str
                xchat.command('say I just tweeted: '+tweet_msg+' '+url)
xchat.hook_command("tweet", tweet, help="/tweet [msg]")
