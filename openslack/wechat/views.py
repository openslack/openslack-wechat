# -*- coding: utf-8 -*-
from __future__ import print_function
import time

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

from wechatpy import WeChatClient
