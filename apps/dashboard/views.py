from django.shortcuts import render
from django.views.generic import TemplateView

from apps.appointments.apis import CallAPI

apis = CallAPI()

# Create your views here.


class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)
