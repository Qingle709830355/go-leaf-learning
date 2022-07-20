from app.app import APP
from game.login.login import Login
from game.chat.chat import Chat

ROUTER_LIST = [
    {
        'path': '/',
        'name': 'login',
        'component': Login(),
    },
    {
        'path': '/chat',
        'name': 'chat',
        'component': Chat(),
    }
]



