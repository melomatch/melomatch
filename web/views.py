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
