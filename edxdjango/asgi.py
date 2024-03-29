"""
ASGI config for edxdjango project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator
from django.conf.urls import url
from post.consumers import ChatConsumer, CommentConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edxdjango.settings')

application = ProtocolTypeRouter({
    'websocket': AllowedHostsOriginValidator(
            AuthMiddlewareStack(
                URLRouter([
                    url(r"comment/(?P<post_id>[0-9]+)", CommentConsumer.as_asgi()),
                    url(r"post/(?P<grp_name>\w+)", ChatConsumer.as_asgi()),
                ])
            )
        )
    })
