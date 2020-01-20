import random

import numpy as np
from monkeylearn import MonkeyLearn

from user_strategy_data import UserStrategyData


def extract_confidence(results):
    res = results.body[0]['classifications'][0]
    return [res['tag_name'], res['confidence']]


def calculate_sentiment(data: UserStrategyData):
    ml = MonkeyLearn('5f0746e7eee9ff88a4135fc126df9cdc17dd54c1')
    model_id = 'cl_pi3C7JiL'

    results = []

    for i, tweet in enumerate(random.choices(data.tweets, k=1)):
        print("Calculating sentiment for tweet {} of {}".format(i + 1, 1))
        res = extract_confidence(ml.classifiers.classify(model_id, [tweet.content]))
        results.append(np.asarray(res))

    result = np.asarray(results)
    analyze_result = {'tag': list(result[:, 0]), 'confidence': list(result[:, 1])}
    return analyze_result
