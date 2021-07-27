from django.urls import path

from .api.views import index_view
from .api.api_views.create_view_set import CreateViewSet
from .api.api_views.info_view_set import InfoViewSet
from .api.api_views.hex2_view_set import Hex2ViewSet

handler404 = "backend.api.views.handler404_redirect"

urlpatterns = [
    # landing page
    path("", index_view, name="index"),
    # API's
    path("api/hex/<str:hex_string>", Hex2ViewSet.as_view()),
    path("api/info", InfoViewSet.as_view()),
    path("api/create", CreateViewSet.as_view()),
]
