from app.app import APP
from game.common.connect import ws_client
from router.router import ROUTER_LIST

ws_client.run()
APP.register_routers(ROUTER_LIST)
APP.run()



