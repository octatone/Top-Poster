import reddit, config

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
        """get the current top song of the month"""

        # get dem posts
        submissions = self.r.get_subreddit('radioreddit').get_top_month(limit=50)
        
        # get the top song submission
        for submission in submissions:
            if submission.url.find('http://www.radioreddit.com/songs/?song=') != -1:
                self.top_submission = submission
                return self.top_submission

        if not self.top_submission:
            return False
