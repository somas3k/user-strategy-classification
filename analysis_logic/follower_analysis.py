from user_strategy_data import UserStrategyData


def get_user_followers(user_data: UserStrategyData):
    followers = 0
    for tweet in user_data.tweets:
        followers += int(tweet.followers)
    followers /= len(user_data.tweets)
    return {
        "user_id": user_data.user_id,
        "label": user_data.label,
        "average_followers": followers
    }
