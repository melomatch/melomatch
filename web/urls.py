from django.urls import path

from web.views import (
    CompareTasteApiView,
    CompareTasteView,
    InstructionView,
    LandingView,
    RequestView,
    TopListView,
)

urlpatterns = [
    path("", LandingView.as_view(), name="landing"),
    path("instruction", InstructionView.as_view(), name="instruction"),
    path("my_top", TopListView.as_view(), name="my-top"),
    path("request/<str:username>", RequestView.as_view(), name="request"),
    path("compare/<str:username>", CompareTasteView.as_view(), name="compare-taste"),
    path("api/compare/<str:username>", CompareTasteApiView.as_view(), name="compare-taste-api"),
]
