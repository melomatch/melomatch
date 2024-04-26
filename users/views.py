import urllib.parse

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView as DjangoLogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import RedirectView, UpdateView

from users.enums import RefreshStatus, RefreshType, Service
from users.forms import PrivacyForm, ProfileForm
from users.models import Refresh, Token, User
from users.services import (
    get_user_by_yandex_data,
    get_user_info_by_yandex_token,
    prepare_yandex_user_data,
)
from web.tasks import load_user_tracks
from web.views import TabsMixin


class YandexOAuthCallbackView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        next_url = kwargs.get("next_url")
        if next_url and next_url not in ["/", "/instruction"]:
            return next_url
        return reverse("profile")

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().get(request, *args, **kwargs)

        next_url = None
        state_param = request.GET.get("state")
        if state_param:
            query_params = urllib.parse.parse_qs(state_param)
            next_url = query_params.get("next", [None])[0]

        token = request.GET.get("access_token")
        if not token:
            return redirect(next_url or "landing")

        result, success = get_user_info_by_yandex_token(token)
        if not success:
            messages.error(request, result)
            return redirect(next_url or "landing")

        user = get_user_by_yandex_data(prepare_yandex_user_data(result), token)
        Token.objects.update_or_create(
            user=user,
            service=Service.YANDEX,
            defaults={"value": token},
            create_defaults={"value": token},
        )
        login(request, user)

        return super().get(request, *args, **kwargs, next_url=next_url)


class LogoutView(DjangoLogoutView):
    next_page = reverse_lazy("landing")


class ProfileView(TabsMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = ProfileForm
    template_name = "users/profile.html"
    success_url = reverse_lazy("profile")
    success_message = "Ваши данные успешно обновлены"

    def get_object(self):
        return User.objects.get(username=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tabs"]["profile"]["active"] = True
        return context


class PrivacyView(TabsMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = PrivacyForm
    template_name = "users/privacy.html"
    success_url = reverse_lazy("privacy")
    success_message = "Ваши данные успешно обновлены"

    def get_object(self):
        return User.objects.get(username=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_link"] = self.request.build_absolute_uri(
            f"/request/{self.request.user.username}"
        )
        context["tabs"]["privacy"]["active"] = True
        return context


class RefreshTracksView(LoginRequiredMixin, SuccessMessageMixin, RedirectView):
    url = reverse_lazy("profile")
    success_message = "Обновление началось. Ваши треки обновятся в течение нескольких минут."

    def post(self, request, *args, **kwargs):
        service, user_id = Service.YANDEX, request.user.id
        token = Token.objects.filter(user_id=user_id, service=service).first()
        if not token:
            messages.error(
                request,
                "К сожалению, у нас нет данных о вашей авторизации. "
                "Попробуйте выйти из аккаунта и войти снова.",
            )

        old_refresh = (
            Refresh.objects.filter(user_id=user_id, service=service).order_by("-updated_at").first()
        )
        if old_refresh and old_refresh.status != RefreshStatus.FINISHED:
            messages.error(request, "Ваши треки уже находятся в процессе обновления.")

        refresh = Refresh.objects.create(user_id=user_id, service=service, type=RefreshType.MANUAL)
        load_user_tracks.apply_async(args=[token.value, user_id, refresh.id])
        return super().post(request, *args, **kwargs)
