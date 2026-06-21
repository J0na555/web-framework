def run_middlewares(middlewares, request, handler):
    def chain(mws, req):
        if not mws:
            return handler(req)

        def next(next_req):
            return chain(mws[1:], next_req)

        return mws[0](req, next)

    return chain(middlewares, request)
