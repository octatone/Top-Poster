from reddit_io import RedditIO
from errors import fatalError
from models import Last
import sys

def main():
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
                rio.postToReddit('music','top on radio reddit: ' + top.title, top.url)
                # store song
                print 'Storing new song ...'
                last.store(top)
                print 'All done here!'
            except:
                e = sys.exc_info()[1]
                print "Error: %s" % e 
    else:
        fatalError('No top song found, time to die.')

main()
