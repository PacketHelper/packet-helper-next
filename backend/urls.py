from django.urls import path

from .api.views import index_view, Hex2ViewSet, InfoViewSet, LikeViewSet, DislikeViewSet

handler404 = "backend.api.views.handler404_redirect"

urlpatterns = [
    # landing page
    path("", index_view, name="index"),
    # API's
    path("api/hex/<str:hex_string>", Hex2ViewSet.as_view()),
    path("api/hex/<str:hex_string>/like", LikeViewSet.as_view(), name="like"),
    path("api/hex/<str:hex_string>/dislike", DislikeViewSet.as_view(), name="dislike"),
    path("api/info", InfoViewSet.as_view()),
]
