import re

from user_strategy_data import UserStrategyData


def calculate_avg_hashtags(data):
    tweets = data.tweets
    counter = 0.0
    for tweet in tweets:
        counter += len(get_hashtags(tweet))
    return counter / len(tweets)


def get_hashtags(tweet):
    return set([re.sub(r"(\W+)$", "", j) for j in set([i for i in tweet.content.split() if i.startswith("#")])])


def analyze_data(data: UserStrategyData):
    return {
        "average_hashtags": calculate_avg_hashtags(data),
        "user_id": data.user_id,
        "label": data.label
    }
