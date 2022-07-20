class RouterController:
    """
    路由控制器
    """
    def __init__(self):
        self.routers = []
        self.app = None

    def register(self, app):
        self.app = app

    def push(self, router: str):
        cookie = None
        if len(self.routers) > 0:
            last_router = self.routers[-1]
            last_component = self.app.routers_dict[last_router]
            if last_component.cache:
                cookie = last_component.cache.COOKIE
            last_component.end()
        self.routers.append(router)
        # 结束上一个路由的页面监听
        # 跳转到下一个
        component = self.app.routers_dict[router]
        if component.cache:
            component.cache.COOKIE = cookie
        component.start()

    def pop(self):
        cookie = None
        # 返回上一级
        if len(self.routers) > 0:
            last_router = self.routers.pop()
            last_component = self.app.routers_dict[last_router]
            if last_component.cache:
                cookie = last_component.cache.COOKIE
            last_component.end()
        router = self.routers[-1]
        component = self.app.routers_dict[router]
        if component.cache:
            component.cache.COOKIE = cookie
        component.start()

    def current_game(self):
        return self.app.routers_dict[self.routers[-1]]

    def current_router(self):
        return self.routers[-1]


