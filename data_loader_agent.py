import os
import csv
import jsonpickle
from typing import Sequence

from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from spade.template import Template

from user_strategy_data import Tweet, UserStrategyData


def translate_tweets(tweets: list) -> Sequence[Tweet]:
    to_return = []
    for row in tweets:
        to_return.append(Tweet(row.get('content'), row.get('publish_date'), row.get('region'), row.get('language'),
                               row.get('following'), row.get('followers'), row.get('updates'), row.get('post_type'),
                               row.get('retweet')))
    return to_return


def load_data() -> Sequence[UserStrategyData]:
    file_amount = len(os.listdir("data/")) - 1
    nickname_tweets = dict()
    for i in range(1, file_amount):
        with open("data/filtered_" + str(i) + ".csv", encoding="utf8") as file:
            # wczytuje każdy wiersz z csv jako oddzielny słownik
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                if row.get('author') in nickname_tweets.keys():
                    nickname_tweets.get(row.get('author')).append(row)
                else:
                    nickname_tweets[row.get('author')] = [row]
    user_strategy_data_list = []
    for user, tweets in nickname_tweets.items():
        tweets_objects = translate_tweets(tweets)
        user_strategy_data_list.append(UserStrategyData(user, tweets_objects, tweets[0].get('account_category')))
    return user_strategy_data_list


names_to_addresses = {
    "sentiment_agent": "sentiment@localhost",
}


class DataLoaderAndBroadcasterAgent(Agent):
    class LoadAndBroadcastBehav(OneShotBehaviour):

        @staticmethod
        def get_message(agent, us_data: UserStrategyData):
            print("Sending data to {}".format(agent))
            msg = Message(names_to_addresses[agent])
            msg.set_metadata("performative", "inform")
            msg.body = us_data
            return msg

        async def run(self):
            print("[DataLoaderAndBroadcasterAgent] loading data...")
            data_list = load_data()
            print("[DataLoaderAndBroadcasterAgent] data loaded")

            for us_data in data_list:
                print("[DataLoaderAndBroadcasterAgent] sending data of user {}".format(us_data.user_id))
                await self.send(self.get_message("sentiment_agent", jsonpickle.encode(us_data)))
                # await self.send(self.get_message("xd", us_data))
                result = await self.receive(timeout=300)
                if result:
                    print(result.body)

    async def setup(self):
        print("DataLoaderAndBroadcasterAgent started")
        b = self.LoadAndBroadcastBehav()
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(b, template)
