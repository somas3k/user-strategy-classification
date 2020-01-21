import time

from activity_analysis_agent import UserActivityAnalysisAgent
from aggregator_agent import AggregatorAgent
from average_hashtags_agent import AverageHashtagsAgent
from average_urls_agent import AverageUrlsAgent
from data_loader_agent import DataLoaderAndBroadcasterAgent
from follower_analysis_agent import UserFollowersAnalysisAgent
from partiality_agent import PartialityAgent
from sentiment_agent import SentimentAnalysisAgent

if __name__ == "__main__":
    agents = [
        AggregatorAgent("aggregator@localhost", "aggregator"),
        SentimentAnalysisAgent("sentiment@localhost", "sentiment"),
        AverageUrlsAgent("averageurls@localhost", "averageurls"),
        AverageHashtagsAgent("averagehashtags@localhost", "averagehashtags"),
        UserFollowersAnalysisAgent("followers@localhost", "followers"),
        UserActivityAnalysisAgent("activity@localhost", "activity"),
        PartialityAgent("partiality@localhost", "partiality"),

        DataLoaderAndBroadcasterAgent("dataloader@localhost", "dataloader")
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
