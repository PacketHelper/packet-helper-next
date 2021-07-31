from django.shortcuts import redirect
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView

# Serve Vue Application
index_view = never_cache(TemplateView.as_view(template_name="index.html"))


def handler404_redirect(request, exception, template_name="404.html"):
    if request.path[:5] == "/hex/":
        return redirect(f"/?redirect={request.path[5:]}")
    return redirect("/")
