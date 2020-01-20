import jsonpickle
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template
import re

from user_strategy_data import UserStrategyData

right_keywords = [
    'right',
    'right-wing',
    'conservative',
    'conservatives',
    'conservatism',
    'tradition',
    'traditionalistic',
    'republican',
    'conformist',
    'monarchy',
    'private'
]

left_keywords = [
    'lgbt',
    'equality',
    'homosexual',
    'gay',
    'lesbian',
    'public',
    'benefits'

]


def calculate_partiality(data, right_keywords):
    pass


def analyze_data(data: UserStrategyData):
    return {
        "right_partiality": calculate_partiality(data, right_keywords),
        "left_partiality": calculate_partiality(data, left_keywords),
        "user_id": data.user_id
    }


class PartialityAgent(Agent):
    class CalculateLeftRightPartiality(CyclicBehaviour):
        async def run(self):
            data_to_analyze = await self.receive(timeout=10)
            if data_to_analyze:
                us_data = jsonpickle.decode(data_to_analyze.body)
                print("[PartialityAgent] received data to analysis for user: {}".format(us_data.user_id))
                analysis = analyze_data(us_data)
                print("[PartialityAgent] analysis completed for user: {}".format(analysis["user_id"]))
                msg = Message(to="aggregator@localhost")  # Instantiate the message
                msg.set_metadata("performative", "inform")
                msg.body = jsonpickle.encode(analysis)
                await self.send(msg)

    async def setup(self):
        print("PartialityAgent started")
        b = self.CalculateLeftRightPartiality()
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(b, template)
