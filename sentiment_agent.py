from spade.agent import Agent
from spade.template import Template
from spade.behaviour import OneShotBehaviour
from spade.message import Message


def analyze_data(data):
    return {}


class SentimentAnalysisAgent(Agent):
    class AnalyzeData(OneShotBehaviour):
        async def run(self):
            while True:
                data_to_analyze = await self.receive(timeout=10)
                if data_to_analyze:
                    analysis = analyze_data(data_to_analyze)
                    msg = Message(to="aggregator@localhost")  # Instantiate the message
                    msg.set_metadata("performative", "request")
                    msg.body = analysis
                    await self.send(msg)

    async def setup(self):
        print("SentimentAnalysisAgent started")
        b = self.AnalyzeData()
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(b, template)
