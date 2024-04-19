from datetime import datetime
from http import HTTPStatus

import requests
from ua_parser.user_agent_parser import ParseUserAgent

from users.enums import Sex
from users.models import User
from web.mappings import browsers_tampermonkey_links
from web.tasks import load_user_tracks


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

    birthday = data["birthday"] or None
    if birthday:
        year, month, day = birthday.split("-")
        year = 1 if year == "0000" else year  # Неизвестные части даты заполняются нулями
        birthday = datetime(int(year), int(month), int(day))
    modified_data["birthday"] = birthday

    sex = data["sex"] or ""
    modified_data["sex"] = Sex(sex[:1].upper())

    return modified_data


def get_user_by_yandex_data(data, token):
    created = False

    try:
        user = User.objects.get(yandex_id=data["yandex_id"])
    except User.DoesNotExist:
        user = User(**data)
        created = True

    user.save()
    if created:
        load_user_tracks.apply_async(args=[token, user.id])

    return user


def get_tampermonkey_link_by_user_agent(user_agent):
    browser_family = ParseUserAgent(user_agent)["family"]
    return browsers_tampermonkey_links.get(browser_family, browsers_tampermonkey_links["Other"])
