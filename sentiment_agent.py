import jsonpickle
from spade.agent import Agent
from spade.template import Template
from spade.behaviour import OneShotBehaviour, CyclicBehaviour
from spade.message import Message
from sentiment_analysis import calculate_sentiment
from user_strategy_data import UserStrategyData


def analyze_data(data: UserStrategyData):
    return {
        "sentiment_analysis": calculate_sentiment(data),
        "user_id": data.user_id
    }


class SentimentAnalysisAgent(Agent):
    class AnalyzeData(CyclicBehaviour):
        async def run(self):
            data_to_analyze = await self.receive(timeout=10)
            if data_to_analyze:
                us_data = jsonpickle.decode(data_to_analyze.body)
                print("[SentimentAnalysisAgent] received data to analysis for user: {}".format(us_data.user_id))
                analysis = analyze_data(us_data)
                print("[SentimentAnalysisAgent] analysis completed for user: {}".format(analysis["user_id"]))
                msg = Message(to="aggregator@localhost")  # Instantiate the message
                msg.set_metadata("performative", "inform")
                msg.body = jsonpickle.encode(analysis)
                await self.send(msg)

    async def setup(self):
        print("SentimentAnalysisAgent started")
        b = self.AnalyzeData()
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(b, template)
