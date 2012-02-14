from reddit_io import RedditIO
from twitter_io import TwitterIO
from errors import fatalError
from models import Last
import sys, time, datetime, re, random

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
    periods = ['month','week']
    tops = []

    print 'Logging in to reddit and retriving top rr song for for the week and month'
    rio = RedditIO()

    for period in periods:
        top = rio.getTopSong(period)
        tops.append(top)
        if top:
            print 'Top song retrieved for', period, top
            # check for old post
            last = Last()
            if last.isStored(top):
                print 'Not a new song.  Done.'
            else:
                print 'Is a new song!'
                # post to reddit
                print 'Posting to reddit ...'
                try:
                    rio.postToReddit('music','top for the %s on radio reddit: %s' % (period, top.title), top.url)
                    print 'All done here!'
                except:
                    e = sys.exc_info()[1]
                    fatalError("Error: %s" % e)
                print 'Posting to twitter ...'
                twit = TwitterIO()
                twit.postToTwitter('New top song: %s %s' % (top.title, top.url))
        else:
            fatalError('No top song found, time to die.')
    # store tops
    last.store(tops)

def hourly():
    """hourly tasks"""
    # WHITELIST RADIOREDDIT.COM IN THE MOD QUEUE
    print 'Logging in ...'
    rio = RedditIO()
    print 'Whitelisting ...'
    rio.whitelistCheck('radioreddit',['radioreddit.com'])

    # TELL PEOPLE TO UPLOAD THEIR SHIT
    print 'Looking for bands posting to music ...'
    new = rio.getNewPosts('music', 100)
    hour_ago = time.mktime((datetime.datetime.now() - datetime.timedelta(hours=1)).timetuple())
    comments = ['Don\'t forget to upload your music to [radio reddit](http://radioreddit.com/uploading)!', 'Put your music on [radio reddit](http://radioreddit.com/uploading)', 'We\'d love to have your stuff on [radio reddit](http://radioreddit.com/uploading)!','If you want to reach more ears, put your music up on [radio reddit](http://radioreddit.com/uploading)!']

    for post in new:
        #print datetime.datetime.fromtimestamp(hour_ago), datetime.datetime.fromtimestamp(post.created_utc), post.title
        if post.created_utc > hour_ago and re.search('(my|our) (band|music|ep|cd|album|song).*free', post.title, re.IGNORECASE) and not re.search('(cover|remix)', post.title, re.IGNORECASE):
            print 'Leaving comment on:'
            print post.created_utc, post.title, '...'
            rio.postComment(post, choice(comments))

main()
