from flask import render_template

class DummyController:

    def __init__(self,template):
        self.template = template

    def dispatch(self, request):
        return render_template(self.template)