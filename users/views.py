from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import RedirectView

from users.services import (
    get_user_by_yandex_data,
    get_user_info_by_yandex_token,
    prepare_yandex_user_data,
)


class YandexOAuthCallbackView(RedirectView):
    # TODO: сменить ссылку на профиль
    url = reverse_lazy("index")

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
