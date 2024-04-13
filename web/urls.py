from django.urls import path

from web.views import InstructionView, LandingView, TopListView

urlpatterns = [
    path("", LandingView.as_view(), name="landing"),
    path("instruction", InstructionView.as_view(), name="instruction"),
    path("top_list", TopListView.as_view(), name="top_list"),
]
