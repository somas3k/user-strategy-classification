from user_strategy_data import UserStrategyData


def analyse_data(user_data: UserStrategyData):
    tweet_size = 0.0
    date = None
    for tweet in user_data.tweets:
        if date is None:
            date = tweet.publish_date
        tweet_size += len(tweet.content)
    tweet_size /= len(user_data.tweets)
    return {
        "user_id": user_data.user_id,
        "label": user_data.label,
        "average_tweet_size": tweet_size,
        "date": date
    }