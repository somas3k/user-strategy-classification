import random
from user_strategy_data import UserStrategyData
import numpy as np
from textblob import TextBlob


def calculate_sentiment(data: UserStrategyData):
    result = []

    for i, tweet in enumerate(random.choices(data.tweets, k=1)):
        print("Calculating sentiment for tweet {} of {}".format(i + 1, 1))
        res = TextBlob(tweet.content)
        result.append(np.asarray(res.sentiment))

    result = np.asarray(result)
    analyze_result = {'polarity': list(result[:, 0]), 'subjectivity': list(result[:, 1])}
    return analyze_result
