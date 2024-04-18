from django.urls import path

from web.views import InstructionView, LandingView, RequestView, TopListView

urlpatterns = [
    path("", LandingView.as_view(), name="landing"),
    path("instruction", InstructionView.as_view(), name="instruction"),
    path("my_top", TopListView.as_view(), name="my_top"),
    path("request/<str:username>", RequestView.as_view(), name="request"),
]
