from django.views.generic import TemplateView
from ua_parser.user_agent_parser import ParseUserAgent

from web.enums import Browser


class IndexView(TemplateView):
    template_name = "web/pages/base.html"


class InstructionView(TemplateView):
    template_name = "web/pages/instruction.html"

    def get(self, request):
        browser_family = ParseUserAgent(request.META["HTTP_USER_AGENT"])["family"]
        context = self.get_context_data()
        try:
            context["browser_family"] = getattr(Browser, browser_family).value
        except AttributeError:
            context["browser_family"] = Browser.Unknown.value
        return self.render_to_response(context)
