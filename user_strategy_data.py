from datetime import datetime
from typing import Sequence


class Tweet:
    def __init__(self, content, publish_date: str, region, language, following, followers, updates, post_type, retweet, urls):
        self.content = content
        self.publish_date = datetime.strptime(publish_date.split(' ')[0], '%m/%d/%Y')
        self.region = region
        self.language = language
        self.following = following
        self.followers = followers
        self.updates = updates
        self.post_type = post_type
        self.retweet = retweet
        self.urls = urls


class UserStrategyData:
    def __init__(self, user_id, tweets: Sequence[Tweet], label) -> None:
        self.user_id = user_id
        self.tweets = tweets
        self.label = label
