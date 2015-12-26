# -*- coding: utf-8 -*-
from __future__ import print_function
import time

from django.conf import settings
from django.http import JsonResponse,HttpResponseForbidden,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

from wechatpy import WeChatClient
from wechatpy.utils import check_signature
from wechatpy.crypto import WeChatCrypto
from wechatpy import parse_message, create_reply
from wechatpy.exceptions import InvalidSignatureException
from wechatpy.exceptions import InvalidAppIdException

def index(request):
    return render(request, 'index.html')


@csrf_exempt
def jsapi_signature(request):
    noncestr = '123456'
    timestamp = int(time.time())
    url = request.POST['url']

    client = WeChatClient(settings.WECHAT_APPID, settings.WECHAT_SECRET)
    ticket = client.jsapi.get_ticket()
    signature = client.jsapi.get_jsapi_signature(
        noncestr,
        ticket['ticket'],
        timestamp,
        url
    )
    ret_dict = {
        'noncestr': noncestr,
        'timestamp': timestamp,
        'url': url,
        'signature': signature,
    }
    return JsonResponse(ret_dict)


@csrf_exempt
def wechat(request):
    """
    此地址为响应微信发送的Token验证，验证服务器配置是否正确
    :param request:
    :return:
    """
    signature = request.GET.get('signature', 'c58469c4151fac046efe180b277c51b1e5b563d3')
    timestamp = request.GET.get('timestamp', '1451138472')
    nonce = request.GET.get('nonce', '1432579014')
    echo_str = request.GET.get('echostr', '2691756735856574460')
    encrypt_type = request.args.get('encrypt_type', '')
    msg_signature = request.args.get('msg_signature', '')
    print('signature:', signature)
    print('timestamp: ', timestamp)
    print('nonce:', nonce)
    print('echo_str:', echo_str)
    print('encrypt_type:', encrypt_type)
    print('msg_signature:', msg_signature)
    try:
        check_signature(settings.WECHAT_TOKEN, signature, timestamp, nonce)
    except InvalidSignatureException:
        return HttpResponseForbidden()
    if request.method == 'GET':
        return echo_str
    else:
        print('Raw message: \n%s' % request.data)
        crypto = WeChatCrypto(settings.WECHAT_TOKEN, settings.EncodingAESKey, settings.WECHAT_APPID)
        try:
            msg = crypto.decrypt_message(
                request.data,
                msg_signature,
                timestamp,
                nonce
            )
            print('Descypted message: \n%s' % msg)
        except (InvalidSignatureException, InvalidAppIdException):
            return HttpResponseForbidden()
        msg = parse_message(msg)
        if msg.type == 'text':
            reply = create_reply(msg.content, msg)
        else:
            reply = create_reply('Sorry, can not handle this for now', msg)
        msg= crypto.encrypt_message(
            reply.render(),
            nonce,
            timestamp)
        print(msg)
        return HttpResponse(msg)


def log(request):
    print('Hello World!')
    return JsonResponse({
        'status': 'ok',
    })
