import tweepy, config, sys

class TwitterIO(object):
    def __init__(self):
        """log in to twitter on creation"""
        # twitter config
        auth = tweepy.OAuthHandler(config.t_consumer_key, config.t_consumer_secret)
        auth.set_access_token(config.t_access_token, config.t_access_token_secret)
        self.api = tweepy.API(auth)

    def postToTwitter(self, txt):
        """post to twitter"""
        self.api.update_status("%s" % txt)
