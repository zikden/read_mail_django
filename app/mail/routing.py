from django.urls import re_path

from .consumers import WSConsumers

ws_urlpatterns = [
    re_path(r'ws/letters/', WSConsumers.as_asgi())
]
