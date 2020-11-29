from django.shortcuts import render

# load the index/about page
from django.views import View


class IndexView(View):
    def get(self, request):
        response = render(request, "index.html")
        return response
