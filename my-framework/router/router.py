class Router:
    def __init__(self):
        self.routes = {}

    def add_route(self, method, path, handler):
        self.routes[(method, path)] = handler

    def get_handler(self, method, path):
        return self.routes.get((method, path), None)

    def resolve(self, method, path):
        return self.get_handler(method, path)
    
# this matches route with handler 
