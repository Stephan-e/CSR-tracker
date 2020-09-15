from django.urls import path

from .views import HomePageView, AboutPageView
# from tracker.views import CompanyPageView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    # path('company/', CompanyPageView.as_view(), name='company'),

]
