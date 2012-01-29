from reddit_io import RedditIO
from twitter_io import TwitterIO
from errors import fatalError
from models import Last
import sys

script, task = sys.argv

def main():
    if task == 'weekday':
        weekDaily()
    elif task == 'hour':
        hourly()
    else:
        print 'No task provided. Shutting down.'

def weekDaily():
    """tasks for weekdays"""
    # POST NEW TOP SONG
    print 'Logging in to reddit and retriving top rr song for the month ...'
    rio = RedditIO()
    top = rio.getTopSong()
    if top:
        print 'Top song retrieved:', top
        # check for old post
        last = Last()
        if last.isStored(top):
            print 'Not a new song.  Done.'
        else:
            print 'Is a new song!'
            # post to reddit
            print 'Posting to reddit ...'
            try:
                rio.postToReddit('music','top on radio reddit: %s' % top.title, top.url)
                # store song
                print 'Storing new song ...'
                last.store(top)
                print 'All done here!'
            except:
                e = sys.exc_info()[1]
                fatalError("Error: %s" % e)
            print 'Posting to twitter ...'
            twit = TwitterIO()
            twit.postToTwitter('New top song: %s %s' % (top.title, top.url))
    else:
        fatalError('No top song found, time to die.')

def hourly():
    """hourly tasks"""
    # WHITELIST RADIOREDDIT.COM IN THE MOD QUEUE
    rio = RedditIO()
    rio.whitelistCheck('radioreddit',['radioreddit.com'])

main()
