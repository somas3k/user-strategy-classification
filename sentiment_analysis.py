import numpy as np
from textblob import TextBlob

from user_strategy_data import UserStrategyData


def calculate_sentiment(data: UserStrategyData):
    result = []

    for tweet in data.tweets:
        res = TextBlob(tweet.content)
        result.append(np.asarray(res.sentiment))
    print("Calculated sentiment for {} tweets".format(len(data.tweets)))

    result = np.asarray(result)
    analyze_result = {'polarity': np.mean(result[:, 0]), 'subjectivity': np.mean(result[:, 1])}
    return analyze_result
