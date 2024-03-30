from django.urls import path

from web.views import LandingView

urlpatterns = [
    path("", LandingView.as_view(), name="landing"),
]
