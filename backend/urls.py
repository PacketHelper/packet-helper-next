from django.urls import path

from .api.views import index_view, Hex2ViewSet, InfoViewSet

handler404 = "backend.api.views.handler404_redirect"

urlpatterns = [
    # landing page
    path("", index_view, name="index"),
    # API's
    path("api/hex/<str:hex_string>", Hex2ViewSet.as_view()),
    path("api/info", InfoViewSet.as_view()),
]
