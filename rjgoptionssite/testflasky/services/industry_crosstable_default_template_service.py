
class IndustryCrosstableDefaultTemplateService:
    def __init__(self):
        self.template_name = "COMMON_TEMPLATE"
        #print("http://127.0.0.1:4999/industry/subscribe?template=" + self.template_name)

    def get_template_owner(self):
        return self.template_name

