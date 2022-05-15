from django.urls import path

from .views import AppointmentListView, HomePageView

app_name = 'dashboard'

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('appointments/', AppointmentListView.as_view(), name='appointment-list')
]
