import jsonpickle
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template

from user_strategy_data import UserStrategyData


def get_user_followers(user_data: UserStrategyData):
    followers = 0
    for tweet in user_data.tweets:
        followers += int(tweet.followers)
    followers /= len(user_data.tweets)
    return {
        "user_id": user_data.user_id,
        "label": user_data.label,
        "average_followers": followers
    }


class UserFollowersAnalysisAgent(Agent):
    class AnalyzeData(CyclicBehaviour):
        async def run(self):
            user_data_encoded = await self.receive(timeout=10)
            if user_data_encoded:
                user_data = jsonpickle.decode(user_data_encoded.body)
                print("[UserFollowersAnalysisAgent] received data to analysis for user: {}".format(user_data.user_id))
                analysis = get_user_followers(user_data)
                print("[UserFollowersAnalysisAgent] analysis completed for user: {}".format(analysis["user_id"]))
                msg = Message(to='aggregator@localhost')
                msg.set_metadata('performative', 'inform')
                msg.body = jsonpickle.encode(analysis)
                await self.send(msg)

    async def setup(self):
        print("UserFollowersAnalysisAgent started")
        b = self.AnalyzeData()
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(b, template)