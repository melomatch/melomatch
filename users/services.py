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
    if not HTTPStatus(response.status_code).is_success:
        return "Не удалось получить информацию о пользователе", False

    return response.json(), True


def prepare_yandex_user_data(data):
    modified_data = {
        "username": data["login"],
        "yandex_id": int(data["id"]),
        "email": data["default_email"],
        "avatar": f"https://avatars.yandex.net/get-yapic/{data["default_avatar_id"]}",
        "first_name": data["first_name"],
        "last_name": data["last_name"],
    }

    birthday = data["birthday"]
    if birthday:
        year, month, day = birthday.split("-")
        year = 1 if year == "0000" else year  # Неизвестные части даты заполняются нулями
        birthday = datetime(int(year), int(month), int(day))
    modified_data["birthday"] = birthday

    sex = data["sex"] or ""
    modified_data["sex"] = Sex(sex[:1].upper())

    return modified_data


def get_user_by_yandex_data(data):
    try:
        user = User.objects.get(yandex_id=data["yandex_id"])
    except User.DoesNotExist:
        user = User(**data)

    user.save()
    return user