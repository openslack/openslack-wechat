# -*- coding: utf-8 -*-
"""
rpc中间件，可以监控rpc的一些状态或者做一些tracelog记录
"""

class ClientMiddleware(object):

    def __init__(self):
        self.called = True

    def client_before_request(self, event):
        self.method = event.name

    def client_after_request(self, req_event, rep_event, exception):
        pass
        # assert req_event is not None
        # assert req_event.name == "crash" or req_event.name == "echoes_crash"
        # self.called = True
        # assert isinstance(exception, zerorpc.RemoteError)
        # assert exception.name == 'RuntimeError'
        # assert 'BrokenEchoModule' in exception.msg
        # assert rep_event.name == 'ERR'

    def client_handle_remote_error(self, event):
        pass

    def client_patterns_list(self, patterns):
        pass

