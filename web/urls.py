from django.urls import path

from web.views import InstructionView, LandingView, RequestView

urlpatterns = [
    path("", LandingView.as_view(), name="landing"),
    path("instruction", InstructionView.as_view(), name="instruction"),
    path("request/<str:username>", RequestView.as_view(), name="request"),
]
