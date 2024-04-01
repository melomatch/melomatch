from django.urls import path

from web.views import IndexView, InstructionView

urlpatterns = [
    path("", LandingView.as_view(), name="landing"),
    path("instruction", InstructionView.as_view(), name="instruction"),
]
