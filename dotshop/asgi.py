"""
ASGI config for dotshop project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
# from django.urls import re_path
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
# from app1 import ChatConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dotshop.settings')

application = get_asgi_application()

# websocket_urlpatterns = [
#     re_path(r'ws/chat/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),
# ]

# application = ProtocolTypeRouter({
#     "http": application,
#     "websocket": AuthMiddlewareStack(
#         URLRouter(
#             websocket_urlpatterns
#         )
#     ),
# })
