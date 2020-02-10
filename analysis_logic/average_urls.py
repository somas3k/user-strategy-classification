from user_strategy_data import UserStrategyData


def calculate_avg_urls(data):
    tweets = data.tweets
    counter = 0.0
    for tweet in tweets:
        counter += len(tweet.urls)
    return counter / len(tweets)


def analyze_data(data: UserStrategyData):
    return {
        "average_urls": calculate_avg_urls(data),
        "user_id": data.user_id,
        "label": data.label
    }



