from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from siteadmin.forms import HighQSiteForm, HighQSiteOwnerMessage


class HighQSiteSearchPage(View):
    @method_decorator(login_required)
    def get(self,request):
        form = HighQSiteForm()
        form2 = HighQSiteOwnerMessage()
        return render(request, 'siteadmin/site_search.html', {'form': form, 'form2':form2})

class HighQSiteSearch(View):
    @method_decorator(login_required)
    def get(self,request):
        search_result = {}
        if 'sitename' in request.GET:
            form = HighQSiteForm(request.GET)
            if form.is_valid():
                search_result = form.search()

        return JsonResponse(search_result)

class HighQSiteAdminMessage(View):
    @method_decorator(login_required)
    def get(self,request):
        message_result = {}
        params = ['email_message','user_id','site_id']
        if params[0] in request.GET and params[1] in request.GET and params[2] in request.GET :
            form = HighQSiteOwnerMessage(request.GET)
            if form.is_valid():
                message_result = form.send()
        else:
            message_result['message'] = 'Not Enough parameters supplied....'

        return JsonResponse(message_result)


