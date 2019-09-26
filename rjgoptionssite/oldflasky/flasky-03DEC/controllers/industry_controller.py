from flask import render_template , jsonify
import json

class IndustryController:

    def __init__(self,industryCrosstableService,visitorDbService,industryCrosstableDefaultTemplateService,template):
        self.industryCrosstableService = industryCrosstableService
        self.visitorDbService = visitorDbService
        self.industryCrosstableDefaultTemplateService = industryCrosstableDefaultTemplateService
        self.template = template
        self.subscribes = {}


    def subscribe(self,request):
        template = request.args["template"]
        self.subscribes[request.remote_addr] = template
        return self.dispatch(request)

    def unsubscribe(self,request):
        if request.remote_addr in self.subscribes:
            del self.subscribes[request.remote_addr]
        return self.dispatch(request)

    def get_visitor(self,request):
        ip = request.remote_addr
        if ip in self.subscribes:
            return self.visitorDbService.getByIp(self.subscribes[ip])
        return self.visitorDbService.getByIp(ip)

    def create_visitor(self,request):
        ip = request.remote_addr
        if ip in self.subscribes:
            visitor = self.visitorDbService.create(self.subscribes[ip])
        else:
            visitor = self.visitorDbService.create(ip)
        return visitor


    def dispatch(self,request):
        visitor = self.get_visitor(request)
        user_industries,user_industry_relations,crosstable = self.industryCrosstableService.get_by_user(visitor)
        return render_template(self.template,user_industries=user_industries,user_industry_relations=user_industry_relations,
                               crosstable=crosstable,visitor=visitor)

    def add(self,request):
        name = request.form.get('new_industry')
        if name is not None and name != '':
            visitor = self.get_visitor(request)
            if visitor is None:
                visitor = self.create_visitor(request)
            if not self.industryCrosstableService.user_have_industry(visitor=visitor,name=name):
                self.industryCrosstableService.add(visitor,name)
        return self.dispatch(request)


    def get_template(self,request):
        visitor = self.get_visitor(request)
        template_code = self.industryCrosstableDefaultTemplateService.get_template_owner()
        template_owner = self.visitorDbService.getByIp(template_code)
        if visitor is None:
            visitor = self.visitorDbService.create(request.remote_addr)

        print("visitor",visitor,"temp code",template_code,"temp owner",template_owner)

        self.industryCrosstableService.get_template(template_owner,visitor)
        return self.dispatch(request)


    def delete(self,request):
        try:
            raw_id = request.form.get('industry_id')
            id = int(raw_id)
            if id is not None:
                visitor = self.get_visitor(request)
                self.industryCrosstableService.delete(id,visitor)
        except Exception as problem:
            pass
        return self.dispatch(request)

    def update_all(self,request):
        try:
            visitor = self.get_visitor(request)
            self.industryCrosstableService.update(request.form,visitor)
        except Exception as error:
            pass
        return self.dispatch(request)








