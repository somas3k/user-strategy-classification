import jsonpickle
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template

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


class AverageUrlsAgent(Agent):
    class CalculateAverageUrls(CyclicBehaviour):
        async def run(self):
            data_to_analyze = await self.receive(timeout=10)
            if data_to_analyze:
                us_data = jsonpickle.decode(data_to_analyze.body)
                print("[AverageUrlsAgent] received data to analysis for user: {}".format(us_data.user_id))
                analysis = analyze_data(us_data)
                print("[AverageUrlsAgent] analysis completed for user: {}".format(analysis["user_id"]))
                msg = Message(to="aggregator@localhost")  # Instantiate the message
                msg.set_metadata("performative", "inform")
                msg.body = jsonpickle.encode(analysis)
                await self.send(msg)

    async def setup(self):
        print("AverageUrlsAgent started")
        b = self.CalculateAverageUrls()
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(b, template)
