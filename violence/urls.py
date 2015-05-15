from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^$', HomePageView.as_view(), name='home'),
]
