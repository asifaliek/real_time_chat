from django.urls import re_path,path
from django.core.asgi import get_asgi_application 

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator

from chat.consumers import ChatConsumer
from personal_chat.personalchat_consumers import PersonalChatConsumer

application = ProtocolTypeRouter({
    "http": get_asgi_application(), 
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter([
                re_path(r"^ws/room/chat/(?P<room_code>[\w.@+-]+)/$", ChatConsumer.as_asgi()), #Change No.3
                re_path(r"^ws/personal/chat/(?P<username>[\w.@+-]+)/$", PersonalChatConsumer.as_asgi()), #Change No.3
           ])
        )
    )
})