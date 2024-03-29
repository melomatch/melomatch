from django.urls import path

from web.views import IndexView, InstructionView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("instruction", InstructionView.as_view(), name="instruction"),
]
