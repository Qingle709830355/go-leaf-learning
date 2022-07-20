from router.router_controller import RouterController


class App:

    routers: list = []
    routers_dict: dict

    def __init__(self):
        self.router = RouterController()
        self._dict_router_list()

    def _dict_router_list(self):
        self.routers_dict = {router['path']: router['component']
                             for router in self.routers}
        self.router.register(self)

    def register_routers(self, router_list):
        self.routers = router_list
        # 转化为dict
        self._dict_router_list()

    def include_router(self, router):
        self.routers.append(router)
        self._dict_router_list()

    def current_game(self):
        self.router.current_game()

    def run(self):
        # 初始化路由控制器
        if self.routers:
            self.router.push('/')


APP = App()