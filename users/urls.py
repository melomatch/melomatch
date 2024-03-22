from django.urls import path

from users.views import YandexOAuthCallbackView

urlpatterns = [
    path("callback/yandex", YandexOAuthCallbackView.as_view(), name="yandex-callback"),
]
