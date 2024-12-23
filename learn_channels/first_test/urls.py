from django.urls import path
from .consumer import Notification
from . import views


# WSGI URLS
urlpatterns = [
    path('', views.home, name='home'),
]

# ASGI URLS
asgi_url = [
    path('ws/first/', Notification.as_asgi(), )
]