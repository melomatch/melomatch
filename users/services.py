from datetime import datetime
from http import HTTPStatus

import requests

from users.enums import Sex
from users.models import User


def get_user_info_by_yandex_token(token):
    url = "https://login.yandex.ru/info"
    headers = {
        "Authorization": f"OAuth {token}",
    }

    response = requests.get(url, headers=headers, timeout=15)
    if HTTPStatus(response.status_code).is_success:
        return "Не удалось получить информацию о пользователе", False

    return response.json(), True


# TODO: функция prepair_yandex_user_data для переименования атрибутов и
#  обработки необычных случаев (тудушки снизу)


def get_user_by_yandex_data(data):
    try:
        user = User.objects.get(yandex_id=int(data["id"]))
    except User.DoesNotExist:
        user = User(
            yandex_id=int(data["id"]),
            username=data["login"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["default_email"],
            # TODO: Обработать следующий случай: "Неизвестные части даты
            #  заполняются нулями, например: 0000-12-23"
            birthday=datetime.strptime(data["birthday"], "%Y-%m-%d"),
            # TODO: Обработать None
            sex=Sex(data["sex"][0].capitalize()),
            avatar=f"https://avatars.yandex.net/get-yapic/{data["default_avatar_id"]}",
        )
    user.save()
    return user
