from http import HTTPStatus

import requests


def get_user_info_by_yandex_token(token):
    url = "https://login.yandex.ru/info"
    headers = {
        "Authorization": f"OAuth {token}",
    }

    response = requests.get(url, headers=headers, timeout=15)
    if HTTPStatus(response.status_code).is_success:
        return "Не удалось получить информацию о пользователе", False

    return response.json(), True
