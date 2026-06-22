class RadixNode:
    __slots__ = ('prefix', 'children', 'handlers', 'param_name', 'wildcard_child')

    def __init__(self, prefix=""):
        self.prefix = prefix
        self.children = []
        self.handlers = {}  
        self.param_name = None
        self.wildcard_child = None


class RadixTree:
    def __init__(self):
        self.root = RadixNode()

    def insert(self, method, path, handler):
        node = self.root
        segments = self._split_path(path)

        # walk each path segment and build the matching radix nodes
        for seg in segments:
            if seg.startswith(':'):
                # parameter segment: reuse or create a param child node
                param_name = seg[1:]
                param_child = self._find_param_child(node)
                if not param_child:
                    param_child = RadixNode()
                    param_child.param_name = param_name
                    node.children.append(param_child)
                node = param_child
            elif seg == '*':
                # wildcard segment: attach handler and stop
                if not node.wildcard_child:
                    node.wildcard_child = RadixNode()
                node.wildcard_child.handlers[method] = handler
                return
            else:
                # static segment: reuse or create a static child node
                child = self._find_child(node, seg)
                if not child:
                    child = RadixNode(seg)
                    node.children.append(child)
                node = child

        node.handlers[method] = handler

    def search(self, method, path):
        node = self.root
        params = {}
        segments = self._split_path(path)

        # walk path segments and choose the best match at each node
        for i, seg in enumerate(segments):
            # check static children first (highest priority)
            child = self._find_child(node, seg)
            if child:
                node = child
                continue

            # check parameter child
            param_child = self._find_param_child(node)
            if param_child:
                params[param_child.param_name] = seg
                node = param_child
                continue

            # check wildcard (lowest priority)
            if node.wildcard_child:
                remaining = '/'.join(segments[i:])
                params['*'] = remaining
                handler = node.wildcard_child.handlers.get(method)
                if handler:
                    return handler, params
                return None, {}

            return None, {}

        # After loop: check if current node has a wildcard child (e.g. /static/ matches /static/*)
        if node.wildcard_child:
            params['*'] = ''
            handler = node.wildcard_child.handlers.get(method)
            if handler:
                return handler, params
            return None, {}

        handler = node.handlers.get(method)
        if handler:
            return handler, params
        return None, {}

    def _split_path(self, path):
        # normalize and split the path into segments
        path = path.strip('/')
        if not path:
            return []
        return path.split('/')

    def _find_child(self, node, prefix):
        # find a static child node for this segment
        for child in node.children:
            if child.prefix == prefix and child.param_name is None:
                return child
        return None

    def _find_param_child(self, node):
        # find a parameter child node if one exists
        for child in node.children:
            if child.param_name is not None:
                return child
        return None
