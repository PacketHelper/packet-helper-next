from django.urls import path

<<<<<<< HEAD
from .api.views import index_view
from .api.api_views.create_view_set import CreateViewSet
from .api.api_views.info_view_set import InfoViewSet
from .api.api_views.hex2_view_set import Hex2ViewSet
=======
from .api.views import index_view, Hex2ViewSet, InfoViewSet, addHex
>>>>>>> Add django db model & add new hexes to it

handler404 = "backend.api.views.handler404_redirect"

urlpatterns = [
    # landing page
    path("", index_view, name="index"),
    # API's
    path("api/hex/<str:hex_string>", Hex2ViewSet.as_view(), addHex),
    path("api/info", InfoViewSet.as_view()),
    path("api/create", CreateViewSet.as_view()),
]
