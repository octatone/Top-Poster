import reddit, config, sys

class RedditIO(object):
    def __init__(self):
        self.top_submission = False
        # create custom gets
        reddit.objects.Subreddit.get_top_month = reddit.helpers._get_sorter('top', t='month')
        reddit.objects.Subreddit.get_top_week = reddit.helpers._get_sorter('top', t='week')

        # reddit config
        self.r = reddit.Reddit(user_agent = config.user_agent)
        self.r.login(config.r_login, config.r_pw)

    def postToReddit(self, subreddit, title, url):
        """post to reddit"""
        self.r.submit(subreddit, title, url=url)

    def postComment(self, submission, comment):
        submission.add_comment(comment)

    def getNewPosts(self, subreddit, limit=50):
        """simply get the new posts in a subreddit"""
        posts = self.r.get_subreddit(subreddit).get_new_by_date()
        return posts

    def getTopSong(self, period='month'):
        """get the current top song for a period in /r/radioreddit"""

        # get dem posts
        if period == 'week':
            submissions = self.r.get_subreddit('radioreddit').get_top_week(limit=50)
        else:
            # default period = month
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
