import jsonpickle

from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template


class AggregatorAgent(Agent):
    class AggregateResultsFromAnalysisAgents(CyclicBehaviour):
        async def run(self):
            print("Aggregator agent running")
            number_of_agents = 3
            i = 0
            analyze_results = []
            user = None
            while i < number_of_agents:
                msg = await self.receive(timeout=180)
                if msg:
                    data = jsonpickle.decode(msg.body)
                    user = data["user_id"]
                    print("Received message from {}".format(msg.sender))
                    analyze_results.append(data)
                i += 1
            msg = Message("dataloader@localhost")
            msg.body = "Analyze for user {} is completed".format(user)
            msg.set_metadata("performative", "inform")
            print(analyze_results)
            await self.send(msg)

    async def setup(self):
        print("AggregatorAgent started")
        b = self.AggregateResultsFromAnalysisAgents()
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(b, template)
