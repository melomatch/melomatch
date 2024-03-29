from django.templatetags.static import static
from django.views.generic import TemplateView


class LandingView(TemplateView):
    template_name = "web/pages/landing.html"

    def get_context_data(self, **kwargs):
        features = [
            {
                "icon": "fa-brands fa-yandex",
                "title": "Вход через Яндекс Музыку",
                "description": "Для использования сервиса вам не нужно регистрироваться "
                "- достаточно войти через Яндекс, после чего вы уже "
                "будете готовы сравнивать музыкальный вкус с другими",
            },
            {
                "icon": "fa-user-group",
                "title": "Сравнивание музыкальных вкусов",
                "description": "Вы можете сравнить вкус, найдя пользователя в "
                "поиске, либо перейдя по ссылке для сравнения, "
                "которую можно создать в профиле",
            },
            {
                "icon": "fa-music",
                "title": "Твой топ артистов и жанров",
                "description": "В профиле можно посмотреть список самых "
                "прослушиваемых тобой артистов и жанров",
            },
        ]
        authors = [
            {
                "name": "addefan",
                "avatar": static("web/images/addefan.png"),
                "role": "Основатель и бэкенд, фронтенд разработчик",
                "github": "https://github.com/addefan",
                "telegram": "https://t.me/addefan",
            },
            {
                "name": "amirdianov",
                "avatar": static("web/images/amirdianov.png"),
                "role": "Бэкенд, фронтенд разработчик",
                "github": "https://github.com/amirdianov",
                "telegram": "https://t.me/diyanovamir",
            },
            {
                "name": "DashaVed",
                "avatar": static("web/images/DashaVed.png"),
                "role": "Бэкенд, фронтенд разработчик",
                "github": "https://github.com/DashaVed",
                "telegram": "https://t.me/d_vedernikova",
            },
        ]
        return super().get_context_data(**kwargs, features=features, authors=authors)
