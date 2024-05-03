from django.urls import path

from users.views import (
    LogoutView,
    PrivacyView,
    ProfileView,
    RefreshTracksView,
    YandexOAuthCallbackView,
)

urlpatterns = [
    path("callback/yandex", YandexOAuthCallbackView.as_view(), name="yandex-callback"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("profile", ProfileView.as_view(), name="profile"),
    path("privacy", PrivacyView.as_view(), name="privacy"),
    path("refresh_tracks", RefreshTracksView.as_view(), name="refresh-tracks"),
]
