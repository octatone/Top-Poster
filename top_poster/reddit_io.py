import reddit, config, sys

class RedditIO(object):
    def __init__(self):
        self.top_submission = False
        # create get_top_month sorter
        reddit.objects.Subreddit.get_top_month = reddit.helpers._get_sorter('top', t='month')

        # reddit config
        self.r = reddit.Reddit(user_agent = config.user_agent)
        self.r.login(config.r_login, config.r_pw)

    def postToReddit(self, subreddit, title, url):
        """post to reddit"""
        self.r.submit(subreddit, title, url=url)

    def getTopSong(self):
        """get the current top song of the month in /r/radioreddit"""

        # get dem posts
        submissions = self.r.get_subreddit('radioreddit').get_top_month(limit=50)
        
        # get the top song submission
        for submission in submissions:
            if submission.url.find('http://www.radioreddit.com/songs/?song=') != -1:
                self.top_submission = submission
                return self.top_submission

        if not self.top_submission:
            return False

    def whitelistCheck(self, subreddit, whitelist):
        """check removed queue for whitelisted domains"""
        modqueue = self.r.get_subreddit(subreddit).get_modqueue(limit=10)
        count = 0
        for removed in modqueue:
            for white in whitelist:
                if removed.domain.find(white) != -1 :
                    print "Approving %s ..." % (removed.title)
                    try:
                        removed.approve()
                        count += 1
                    except:
                        e = sys.exc_info()[1]
                        print "Error: %s" % e
        print "%s posts approved." % (count)
