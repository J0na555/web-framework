from router.radix_tree import RadixTree


class Router:
    def __init__(self):
        self.tree = RadixTree()

    def add_route(self, method, path, handler):
        self.tree.insert(method, path, handler)

    def resolve(self, method, path):
        return self.tree.search(method, path)


# this matches route with handler
