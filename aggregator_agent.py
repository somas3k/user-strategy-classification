import jsonpickle
import csv

from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template


def flatten_list_to_dict(analysis_results):
    flat = {}
    for result in analysis_results:
        for key in result.keys():
            if key not in flat:
                flat[key] = result[key]
    return flat


def save_results(analyze_results):
    flat_results = flatten_list_to_dict(analyze_results)
    with open('results.csv', 'a', newline='') as results:
        field_names = [
            'user_id', 'tweets', 'retweets', 'average_hashtags', 'average_urls', 'average_followers',
            'right_partiality', 'left_partiality', 'polarity', 'subjectivity', 'average_tweet_size', 'label'
        ]
        writer = csv.DictWriter(results, fieldnames=field_names)
        writer.writerow(flat_results)


class AggregatorAgent(Agent):
    class AggregateResultsFromAnalysisAgents(CyclicBehaviour):
        async def run(self):
            print("Aggregator agent running")
            number_of_agents = 7
            i = 0
            analyze_results = []
            user = None
            label = None
            while i < number_of_agents:
                msg = await self.receive(timeout=180)
                if msg:
                    data = jsonpickle.decode(msg.body)
                    user = data["user_id"] if user is None else user
                    label = data["label"] if label is None else label
                    print("Received message from {}".format(msg.sender))
                    analyze_results.append(data)
                i += 1
            msg = Message("dataloader@localhost")
            msg.body = "Analyze for user {} is completed".format(user)
            msg.set_metadata("performative", "inform")
            print(analyze_results)
            save_results(analyze_results)
            await self.send(msg)

    async def setup(self):
        print("AggregatorAgent started")
        with open('results.csv', 'w', newline='') as results:
            field_names = [
                'user_id', 'tweets', 'retweets', 'average_hashtags', 'average_urls', 'average_followers',
                'right_partiality', 'left_partiality', 'polarity', 'subjectivity', 'average_tweet_size', 'label'
            ]
            writer = csv.DictWriter(results, fieldnames=field_names)
            writer.writeheader()
        b = self.AggregateResultsFromAnalysisAgents()
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(b, template)
