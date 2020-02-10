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
    analyze_result = np.mean(result[:, 0]), np.mean(result[:, 1])
    return analyze_result


def analyze_data(data: UserStrategyData):
    sentiment = calculate_sentiment(data)
    return {
        "polarity": sentiment[0],
        "subjectivity": sentiment[1],
        "user_id": data.user_id,
        "label": data.label
    }
