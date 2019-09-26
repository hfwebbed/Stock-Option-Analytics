from controllers.dummy_controller import DummyController

class ProfitController(DummyController):
    def __init__(self,template):
        DummyController.__init__(self,template)
        #super(ProfitController, self).__init__(template)