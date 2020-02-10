from user_strategy_data import UserStrategyData


def get_user_statistics(user_data: UserStrategyData):
    tweets_no = 0
    retweets_no = 0
    tweets = user_data.tweets
    tweets.sort(key=lambda data: data.publish_date)

    for tweet in tweets:
        retweets_no += int(tweet.retweet)
        tweets_no += 1 - int(tweet.retweet)
    start_date = tweets[0].publish_date
    end_date = tweets[-1].publish_date
    days = (end_date - start_date).days + 1
    return {
        "user_id": user_data.user_id,
        "label": user_data.label,
        "average_tweets_daily": tweets_no / days,
        "average_retweets_daily": retweets_no / days,
    }
