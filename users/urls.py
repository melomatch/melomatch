from django.urls import path

from users.views import LogoutView, YandexOAuthCallbackView

urlpatterns = [
    path("callback/yandex", YandexOAuthCallbackView.as_view(), name="yandex-callback"),
    path("logout", LogoutView.as_view(), name="logout"),
]
