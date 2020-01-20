import jsonpickle
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template
import re

from user_strategy_data import UserStrategyData


def calculate_avg_hashtags(data):
    tweets = data.tweets
    counter = 0.0
    for tweet in tweets:
        counter += len(get_hashtags(tweet))
    return counter / len(tweets)


def get_hashtags(tweet):
    return set([re.sub(r"(\W+)$", "", j) for j in set([i for i in tweet.content.split() if i.startswith("#")])])


def analyze_data(data: UserStrategyData):
    return {
        "average_hashtags": calculate_avg_hashtags(data),
        "user_id": data.user_id
    }


class AverageHashtagsAgent(Agent):
    class CalculateAverageHashtags(CyclicBehaviour):
        async def run(self):
            data_to_analyze = await self.receive(timeout=10)
            if data_to_analyze:
                us_data = jsonpickle.decode(data_to_analyze.body)
                print("[AverageHashtagsAgent] received data to analysis for user: {}".format(us_data.user_id))
                analysis = analyze_data(us_data)
                print("[AverageHashtagsAgent] analysis completed for user: {}".format(analysis["user_id"]))
                msg = Message(to="aggregator@localhost")  # Instantiate the message
                msg.set_metadata("performative", "inform")
                msg.body = jsonpickle.encode(analysis)
                await self.send(msg)

    async def setup(self):
        print("AverageHashtagsAgent started")
        b = self.CalculateAverageHashtags()
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(b, template)
