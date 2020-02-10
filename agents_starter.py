import time

from spade.container import Container

from analysis_logic.sentiment_analysis import analyze_data as sentiment_analyse
from analysis_logic.average_urls import analyze_data as urls_analysis
from analysis_logic.average_hashtags import analyze_data as hashtags_analysis
from analysis_logic.follower_analysis import get_user_followers as followers_analysis
from analysis_logic.activity_analysis import get_user_statistics as activity_analysis
from analysis_logic.partiality import analyze_data as partiality_analysis
from analysis_logic.tweet_size import analyse_data as tweet_size_analysis
from agents.aggregator_agent import AggregatorAgent
from agents.data_analysis_agent import DataAnalysisAgent
from agents.data_loader_agent import DataLoaderAndBroadcasterAgent

if __name__ == "__main__":
    agents = [
        AggregatorAgent("aggregator@localhost", "aggregator"),
        DataAnalysisAgent("sentiment@localhost", "sentiment", 'Sentiment', sentiment_analyse),
        DataAnalysisAgent("averageurls@localhost", "averageurls", 'AverageUrls', urls_analysis),
        DataAnalysisAgent("averagehashtags@localhost", "averagehashtags", 'AverageHashtags', hashtags_analysis),
        DataAnalysisAgent("followers@localhost", "followers", 'Followers', followers_analysis),
        DataAnalysisAgent("activity@localhost", "activity", 'Activity', activity_analysis),
        DataAnalysisAgent("partiality@localhost", "partiality", 'Partiality', partiality_analysis),
        DataAnalysisAgent("tweetsize@localhost", "tweetsize", 'TweetSize', tweet_size_analysis),

        DataLoaderAndBroadcasterAgent("dataloader@localhost", "dataloader", byDateDivision=False, quarterly=False)
    ]
    for agent in agents:
        future = agent.start()
        future.result()

    while agents[0].is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            for agent in agents:
                agent.stop()
            break
    print("Agents finished")
