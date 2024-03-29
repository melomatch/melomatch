from django.views.generic import TemplateView

from web.enums import Browser


class IndexView(TemplateView):
    template_name = "web/pages/base.html"


class InstructionView(TemplateView):
    template_name = "web/pages/instruction.html"

    def get(self, request):
        user_agent = request.META["HTTP_USER_AGENT"]
        context = self.get_context_data()
        if "Chrome" in user_agent:
            context["browser"] = Browser.CHROME.value
        elif "Safari" in user_agent:
            context["browser"] = Browser.SAFARI.value
        elif "Firefox" in user_agent:
            context["browser"] = Browser.FIREFOX.value
        elif "Opera" in user_agent:
            context["browser"] = Browser.OPERA.value
        else:
            context["browser"] = Browser.UNKNOWN.value
        return self.render_to_response(context)
