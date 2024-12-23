"""
ASGI config for learn_channels project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack
from first_test.urls import asgi_url

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'learn_channels.settings')

application = get_asgi_application()

asgi_application = ProtocolTypeRouter({
    'http': application, 
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(URLRouter(asgi_url))
    )

})

