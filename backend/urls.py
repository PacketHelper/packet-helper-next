from django.urls import path

<<<<<<< HEAD
from .api.views import index_view
from .api.api_views.create_view_set import CreateViewSet
from .api.api_views.info_view_set import InfoViewSet
from .api.api_views.hex2_view_set import Hex2ViewSet
from .api.api_views.dislike_view_set import DislikeViewSet
from .api.api_views.Like_view_set import LikeViewSet
=======
from .api.views import index_view, Hex2ViewSet, InfoViewSet, LikeViewSet, DislikeViewSet
>>>>>>> aa42ec13cf4d36b2668ba32ac556c025af05fc85

handler404 = "backend.api.views.handler404_redirect"

urlpatterns = [
    # landing page
    path("", index_view, name="index"),
    # API's
    path("api/hex/<str:hex_string>", Hex2ViewSet.as_view()),
    path("api/hex/<str:hex_string>/like", LikeViewSet.as_view(), name="like"),
    path("api/hex/<str:hex_string>/dislike", DislikeViewSet.as_view(), name="dislike"),
    path("api/info", InfoViewSet.as_view()),
    path("api/create", CreateViewSet.as_view()),
]
