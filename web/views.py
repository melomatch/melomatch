from django.views.generic import TemplateView

from users.services import get_browser_store_link


class IndexView(TemplateView):
    template_name = "web/pages/base.html"


class InstructionView(TemplateView):
    template_name = "web/pages/instruction.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["browser_link"] = get_browser_store_link(self.request)
        return context
