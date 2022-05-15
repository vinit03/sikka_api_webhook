from django.db.models import Q
from django.shortcuts import render
from django.views.generic import ListView, TemplateView

from apps.appointments.models import Appointment

# Create your views here.


class HomePageView(TemplateView):
    template_name = 'home.html'
    extra_context = dict(page_title="Welcome")

    def get_context_data(self, **kwargs):
        return super(HomePageView, self).get_context_data(**kwargs)


class AppointmentListView(ListView):
    model = Appointment
    paginate_by = 15
    template_name = 'list.html'
    extra_context = dict(page_title="Search")
    context_object_name = 'appointments'
    ordering = ('-date',)

    def get_context_data(self, **kwargs):
        context = super(AppointmentListView, self).get_context_data(**kwargs)
        applied_filters = self.request.GET
        context['applied_filters'] = applied_filters
        return context

    def get_queryset(self):
        queryset = super(AppointmentListView, self).get_queryset()

        search_query = self.request.GET.get('q', '')
        lookups = Q()

        if search_query:
            lookups = lookups & Q(patient_name__icontains=search_query)

        queryset = queryset.filter(lookups)
        return queryset
