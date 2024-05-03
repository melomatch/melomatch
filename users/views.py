import urllib.parse

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView as DjangoLogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, RedirectView, UpdateView

from users.enums import RefreshStatus, RefreshType, Service
from users.forms import PrivacyForm, ProfileForm
from users.models import Refresh, Token, User
from users.services import (
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

        user_data = prepare_yandex_user_data(result)
        user, created = User.objects.get_or_create(
            yandex_id=user_data.pop("yandex_id"), defaults=user_data
        )
        Token.objects.update_or_create(
            user=user,
            service=Service.YANDEX,
            defaults={"value": token},
            create_defaults={"value": token},
        )

        if created:
            refresh = Refresh.objects.create(
                user=user, service=Service.YANDEX, type=RefreshType.AUTO
            )
            load_user_tracks.apply_async(args=[token, user.id, refresh.id])

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
        context["refresh"] = (
            Refresh.objects.filter(user=self.request.user, service=Service.YANDEX)
            .order_by("-updated_at")
            .first()
        )
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


class RefreshTracksView(LoginRequiredMixin, RedirectView):
    url = reverse_lazy("profile")

    def post(self, request, *args, **kwargs):
        service, user_id = Service.YANDEX, request.user.id
        token = Token.objects.filter(user_id=user_id, service=service).first()
        if not token:
            messages.error(
                request,
                "К сожалению, у нас нет данных о вашей авторизации. "
                "Попробуйте выйти из аккаунта и войти снова.",
            )
            return super().post(request, *args, **kwargs)

        old_refresh = (
            Refresh.objects.filter(user_id=user_id, service=service).order_by("-updated_at").first()
        )
        if old_refresh and old_refresh.status != RefreshStatus.FINISHED:
            messages.error(request, "Ваши треки уже находятся в процессе обновления.")
            return super().post(request, *args, **kwargs)

        refresh = Refresh.objects.create(user_id=user_id, service=service, type=RefreshType.MANUAL)
        load_user_tracks.apply_async(args=[token.value, user_id, refresh.id])
        messages.info(
            request, "Обновление началось. " "Ваши треки обновятся в течение нескольких минут."
        )
        return super().post(request, *args, **kwargs)


class SearchUserView(LoginRequiredMixin, ListView):
    model = User
    template_name = "users/search.html"
    context_object_name = "users"
    paginate_by = 20

    def get_queryset(self):
        queryset = self.model.objects.filter(~Q(id=self.request.user.id), is_private=False)
        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(
                Q(username__icontains=query)
                | Q(first_name__icontains=query)
                | Q(last_name__icontains=query)
            )
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        return context | {"query_params": dict(self.request.GET)}
