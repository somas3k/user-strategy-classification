from spade.agent import Agent
from spade.behaviour import OneShotBehaviour


class AggregatorAgent(Agent):
    class AggregateResultsFromAnalysisAgents(OneShotBehaviour):
        async def run(self):
            pass

    async def setup(self):
        pass
