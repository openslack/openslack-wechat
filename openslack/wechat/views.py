# -*- coding: utf-8 -*-
from __future__ import print_function
import time

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

from wechatpy import WeChatClient

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from wechat import api
from .models import Member

def get_member(request):
    code = request.GET['code']
    state = request.GET['state']

    wx = api.Member()
    info = wx.get_user_info(code)
    try:
        member = Member.objects.get(openid=info['openid'])
    except Member.DoesNotExist:
        member = Member(
            name = info['nickname'],
            openid = info['openid'],
            city = info['city'],
        )
        member.save()
    request.session['wechat_member_id'] = member.id
    return HttpResponseRedirect(state)

def clear_session(request):
    request.session.flush()
    return HttpResponse('<h1>success</h1>')
