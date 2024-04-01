from django.templatetags.static import static
from django.views.generic import TemplateView

from users.services import get_tampermonkey_link_by_user_agent


class IndexView(TemplateView):
    template_name = "web/pages/base.html"


class InstructionView(TemplateView):
    template_name = "web/pages/instruction.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tampermonkey_link"] = get_tampermonkey_link_by_user_agent(
            self.request.META["HTTP_USER_AGENT"],
        )
        return context

      
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
                "title": "Сравнение музыкальных вкусов",
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
        questions = [
            {
                "text": "Зачем для работы приложения нужно устанавливать расширение?",
                "answer": "Яндекс не даёт возможность разработчикам создать приложение, "
                "через которое бы вы могли авторизоваться, а мы получить нужные "
                "для работы сервиса данные и отправить обратно на этот сайт. "
                "Вместо этого нам приходится использовать приложение Яндекса, "
                "которое отправляет вас на сайт Яндекс Музыки, а не на этот. "
                "Наше расширение ловит этот момент, и вместо того, чтобы попасть "
                "на сайт Яндекс Музыки, вы попадаете на наш сайт, а мы получаем нужные данные.",
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
        return super().get_context_data(
            **kwargs, features=features, authors=authors, questions=questions
        )
