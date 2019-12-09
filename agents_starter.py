from sentiment_agent import SentimentAnalysisAgent

if __name__ == "__main__":
    sentiment_agent = SentimentAnalysisAgent("sentiment@localhost", "sentiment")
    future = sentiment_agent.start()
    future.result() # wait for receiver agent to be prepared.

    print("Agents finished")
