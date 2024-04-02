from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView as DjangoLogoutView
from django.contrib.messages.views import SuccessMessageMixin
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
            return redirect("landing")

        result, success = get_user_info_by_yandex_token(token)
        if not success:
            messages.error(request, result)
            return redirect("landing")

        user = get_user_by_yandex_data(prepare_yandex_user_data(result))
        login(request, user)

        return super().get(request, *args, **kwargs)


class LogoutView(DjangoLogoutView):
    next_page = reverse_lazy("landing")


class ProfileView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = ProfileForm
    template_name = "users/profile.html"
    success_url = reverse_lazy("profile")
    success_message = "Ваши данные успешно обновлены"

    def get_object(self):
        return User.objects.get(username=self.request.user)
