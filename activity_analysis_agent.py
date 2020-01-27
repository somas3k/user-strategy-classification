import jsonpickle
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour
from spade.message import Message
from spade.template import Template
from datetime import datetime

from user_strategy_data import UserStrategyData


def get_user_statistics(user_data: UserStrategyData):
    tweets_no = 0
    retweets_no = 0
    for tweet in user_data.tweets:
        retweets_no += int(tweet.retweet)
        tweets_no += 1 - int(tweet.retweet)
    start_date = datetime.strptime(user_data.tweets[0].publish_date, '%m/%d/%Y %H:%M')
    end_date = datetime.strptime(user_data.tweets[len(user_data.tweets) - 1].publish_date, '%m/%d/%Y %H:%M')
    days = (end_date - start_date).days
    return {
        "user_id": user_data.user_id,
        "label": user_data.label,
        "average_tweets_daily": tweets_no/days,
        "average_retweets_daily": retweets_no/days,
    }


class UserActivityAnalysisAgent(Agent):
    class AnalyzeData(CyclicBehaviour):
        async def run(self):
            user_data_encoded = await self.receive(timeout=10)
            if user_data_encoded:
                user_data = jsonpickle.decode(user_data_encoded.body)
                print("[UserActivityAnalysisAgent] received data to analysis for user: {}".format(user_data.user_id))
                statistics = get_user_statistics(user_data)
                print("[UserActivityAnalysisAgent] analysis completed for user: {}".format(statistics["user_id"]))
                msg = Message(to='aggregator@localhost')
                msg.set_metadata('performative', 'inform')
                msg.body = jsonpickle.encode(statistics)
                await self.send(msg)

    async def setup(self):
        print("UserActivityAnalysisAgent started")
        b = self.AnalyzeData()
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(b, template)
