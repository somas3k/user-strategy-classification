import jsonpickle
from datetime import datetime
from spade.agent import Agent
from spade.template import Template
from spade.behaviour import OneShotBehaviour, CyclicBehaviour
from spade.message import Message
from user_strategy_data import UserStrategyData

def get_user_followers(user_data: UserStrategyData):
    tweet_size = 0.0
    for tweet in user_data.tweets:
        tweet_size += len(tweet.content)
    tweet_size /= len(user_data.tweets)
    return {
        "user_id": user_data.user_id,
        "tweet_size": tweet_size
    }

class UserTweetSizeAnalysisAgent(Agent):
    class AnalyzeData(OneShotBehaviour):
        async def run(self):
            user_data_encoded = await self.receive(timeout=10)
            if user_data_encoded:
                user_data = jsonpickle.decode(user_data_encoded.body)
                print("[UserTweetSizeAnalysisAgent] received data to analysis for user: {}".format(user_data.user_id))
                analysis = get_user_followers(user_data)
                print("[UserTweetSizeAnalysisAgent] analysis completed for user: {}".format(analysis["user_id"]))                
                msg = Message(to='aggregator@localhost')
                msg.set_metadata('performative', 'inform')
                msg.body = jsonpickle.encode(analysis)
                await self.send(msg)

    async def setup(self):
        print("UserTweetSizeAnalysisAgent started")
        b = self.AnalyzeData()
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(b, template)