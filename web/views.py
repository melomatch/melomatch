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
        return super().get_context_data(**kwargs, features=features)
