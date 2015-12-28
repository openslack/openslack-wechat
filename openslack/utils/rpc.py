# -*- coding: utf-8 -*-
import zerorpc
from .middleware import ClientMiddleware


class ZeroRPC:
    location = "tcp://127.0.0.1:4242"

    def __init__(self, location=None, timeout=10):
        if not location:
            location = self.location
        ctx = zerorpc.Context()
        middleware = ClientMiddleware()
        ctx.register_middleware(middleware)
        self.client = zerorpc.Client(connect_to=location, timeout=timeout, context=ctx)

    @staticmethod
    def client(self):
        return self.client