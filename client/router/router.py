from app.app import APP
from game.login.login import Login
from game.chat.chat import Chat
from game.hall.hall import Hall

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
    },
    {
        'path': '/hall',
        'name': 'hall',
        'component': Hall(),
    },
    {
        'path': '/chathall',
        'name': 'hall',
        'component': Hall(),
    }
]



