import jsonpickle
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template


class DataAnalysisAgent(Agent):
    def __init__(self, jid, password, analysis_type, analyse_data_func):
        super().__init__(jid, password)
        self.analysis_type = analysis_type
        self.analyse_data_func = analyse_data_func

    class PerformAnalysis(CyclicBehaviour):
        def __init__(self, analysis_type, analyse_data_func):
            super().__init__()
            self.analyse_data_func = analyse_data_func
            self.analysis_type = analysis_type

        async def run(self):
            data_to_analyze = await self.receive(timeout=10)
            if data_to_analyze:
                us_data = jsonpickle.decode(data_to_analyze.body)
                print("[{}] received data to analysis for user: {}".format(self.analysis_type, us_data.user_id))
                analysis = self.analyse_data_func(us_data)
                print("[{}] analysis completed for user: {}".format(self.analysis_type, analysis["user_id"]))
                msg = Message(to="aggregator@localhost")  # Instantiate the message
                msg.set_metadata("performative", "inform")
                msg.body = jsonpickle.encode(analysis)
                await self.send(msg)

    async def setup(self):
        print("{} started".format(self.analysis_type))
        b = self.PerformAnalysis(self.analysis_type, self.analyse_data_func)
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(b, template)
