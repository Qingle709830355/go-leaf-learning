import websocket
import time
import threading

from app.app import APP
from utils.utils import decode_msg


class WebsocketClient(object):
    """docstring for WebsocketClient"""

    def __init__(self, address):
        super(WebsocketClient, self).__init__()
        self.address = address
        self.is_running = False
        self.is_close = False

    def on_message(self, ws, message):
        # 接收客户端消息
        msg_class = decode_msg(message)
        game_class = APP.router.current_game()
        game_class.cache.save(msg_class)

    def on_error(self, ws, error):
        print("client error:", error)

    def on_close(self, ws, *args, **kwargs):
        print("### client closed ###")
        self.ws.close()
        self.is_running = False
        self.is_close = True
        self.ws.keep_running = False

    def on_open(self, ws):
        self.is_running = True
        print("on open")

    def close_connect(self):
        self.ws.close()

    def send_message(self, message):
        try:
            self.ws.send(message)
        except BaseException as err:
            pass

    def run(self):
        websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp(self.address,
                                         on_message=self.on_message,
                                         on_close=self.on_close,
                                         on_error=self.on_error)
        self.ws.on_open = lambda ws: self.on_open(ws)
        self.is_running = False
        while not self.is_running:
            if not self.is_running:
                self.ws.run_forever()
            if self.is_close:
                break
            time.sleep(3)


class WSClient(object):
    def __init__(self, address):
        super(WSClient, self).__init__()
        self.client = WebsocketClient(address)
        self.client_thread = None

    def run(self):
        self.client_thread = threading.Thread(target=self.run_client)
        self.client_thread.start()

    def run_client(self):
        self.client.run()

    def send_message(self, message):
        self.client.send_message(message)

    def close(self):
        self.client.close_connect()


ws_client = WSClient("ws://localhost:3653/chat/asdasdsdasd")
