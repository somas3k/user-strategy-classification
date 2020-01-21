import itertools

import jsonpickle
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template
import re
from nltk.util import ngrams

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
    'private',
    'undocumented immigrant',
    'illegal immigrant',
    'all lives matter',
    'pro-life',
    'muslims',
    'extremists',
    'islamist',
    'authority',
    'hierarchy',
    'order',
    'lower taxes',
    'lower tax rates',
    'less regulations',
    'less regulation',
    'reduced government',
    'balanced budget',
    'private healthcare',
    'strong border',
    'stronger boarder patrol',
    'private education',
    'private school'
    'private schools',
    'against abortion',
    'free market',
    'republican party',
    'republican',
    'republicans',
    'constitutional party',
    'constitutional',
    'constitutionals',
    'national review',
    'fox news',
    'wall street journal',
    'washington times',
    'capitalism',
    'limited government',
    'personal property rights',
    'death penalty'
]

left_keywords = [
    'lgbt',
    'lgbtq',
    'equality',
    'homosexual',
    'gay',
    'lesbian',
    'public',
    'benefits',
    'minority',
    'minorities',
    'BLM',
    'black lives matter',
    'white privilege',
    'racism',
    'pro-choice',
    'feminist',
    'fraternity',
    'progress',
    'refugees',
    'liberal',
    'higher taxes',
    'higher tax rates',
    'social',
    'social programs',
    'regulations',
    'free healthcare',
    'public education',
    'public school',
    'public schools',
    'unpenalized abortion',
    'stem cell',
    'stem cell research',
    'gay marriage',
    'support gay marriage',
    'allow gay marriage',
    'anti-discrimination',
    'anti-discrimination laws',
    'against workplace discrimination',
    'ban economic activity',
    'democratic party',
    'green',
    'socialist',
    'new york times',
    'msnbc',
    'washington post',
    'cnn',
    'social democracy',
    'federalism',
    'communism',
    'collectivism',
    'marxism',
    'marx',
    'engels',
    'einstein',
    'obama',
    'hollande',
    'economic equality',
    'gun control',
    'environmental protection',
    'expanded educational opportunity',
    'against death penalty'
]


def calculate_partiality(data, keywords):
    counter = 0
    for tweet in data.tweets:
        s = tweet.content.lower()
        s = re.sub(r'[^a-zA-Z0-9\s]', ' ', s)
        tokens = [token.lower() for token in s.split(" ") if token != ""]
        ngrams_tokens = [list(ngrams(tokens, 1)), list(ngrams(tokens, 2)), list(ngrams(tokens, 3))]
        merged = list(itertools.chain.from_iterable(ngrams_tokens))
        joined = [" ".join(token) for token in merged]

        for token in joined:
            if token in keywords:
                counter += 1
    return counter / len(data.tweets)


def analyze_data(data: UserStrategyData):
    return {
        "right_partiality": calculate_partiality(data, right_keywords),
        "left_partiality": calculate_partiality(data, left_keywords),
        "user_id": data.user_id,
        "label": data.label
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
