# -*- coding: utf-8 -*-
from utils.rpc import ZeroRPC
from django.conf import settings

location = "tcp://127.0.0.1:4242"

# client.add(1, 4, async=True)

class QA:
    def __init__(self):
        self.client=ZeroRPC.client

    def get(self, id):
        return self.client.qa.get(id).get()

    def post(self):
        self.client.qa.save("title", "content", "wechat", "submit_time", async=True)
        if self.client == "success":
            return True
        else:
            return False

    def list(self, page=1, num=100):
        self.client.qa.list(page,num)
        if self.client == "success":
            return True
        else:
            return False

    def filter(self, params={}):
        self.client.qa.filter(params, async=True)
        if self.client == "success":
            return True
        else:
            return False
