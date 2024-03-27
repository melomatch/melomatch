from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView as DjangoLogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import RedirectView, UpdateView

from users.forms import ProfileForm
from users.models import User
from users.services import (
    get_user_by_yandex_data,
    get_user_info_by_yandex_token,
    prepare_yandex_user_data,
)


class YandexOAuthCallbackView(RedirectView):
    url = reverse_lazy("profile")

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().get(request, *args, **kwargs)

        token = request.GET.get("access_token")
        if not token:
            return redirect("index")

        result, success = get_user_info_by_yandex_token(token)
        if not success:
            messages.error(request, result)
            return redirect("index")

        user = get_user_by_yandex_data(prepare_yandex_user_data(result))
        login(request, user)

        return super().get(request, *args, **kwargs)


class LogoutView(DjangoLogoutView):
    next_page = reverse_lazy("index")


class ProfileView(LoginRequiredMixin, UpdateView):
    form_class = ProfileForm
    template_name = "users/profile.html"

    def get_object(self):
        return User.objects.get(username=self.request.user)

    def get_success_url(self):
        return reverse_lazy("profile")

    def get_context_data(self):
        return {
            **super(__class__, self).get_context_data(),
            "avatar_url": f"{self.get_object().avatar}/islands-200",
        }
