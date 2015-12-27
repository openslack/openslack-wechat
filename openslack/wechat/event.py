# -*- coding: utf-8 -*-
from django.db import models
from .models import MenuButton

EVENT_TYPE = (
    ('subscribe', '订阅'),
    ('unsubscribe', '取消订阅'),
    ('scan', '关注/取消关注事件'),
    ('click', '自定义菜单事件'),
    ('location', '上报地理位置事件'),
    ('view', '点击菜单跳转链接时的事件'),
)


class SubscribeEvent(models.Model):
    message = models.ForeignKey('Message', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="信息")
    event = models.CharField(max_length=20, choices=EVENT_TYPE)
    event_key = models.CharField(max_length=20, verbose_name='事件KEY值，qrscene_为前缀，后面为二维码的参数值')
    ticket = models.CharField(max_length=20, verbose_name='二维码的ticket，可用来换取二维码图片')

    class Meta:
        ordering = ['-id']
        verbose_name_plural = verbose_name = u"用户订阅事件"


class ScanEvent(models.Model):
    message = models.ForeignKey('Message', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="信息")
    event = models.CharField(max_length=20, choices=EVENT_TYPE)
    event_key = models.CharField(max_length=20, verbose_name='事件KEY值，qrscene_为前缀，后面为二维码的参数值')
    ticket = models.CharField(max_length=20, verbose_name='二维码的ticket，可用来换取二维码图片')

    class Meta:
        ordering = ['-id']
        verbose_name_plural = verbose_name = u"用户扫描二维码事件"


class LocationEvent(models.Model):
    message = models.ForeignKey('Message', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="信息")
    event = models.CharField(max_length=20, choices=EVENT_TYPE)
    event_key = models.CharField(max_length=20, verbose_name='事件KEY值，qrscene_为前缀，后面为二维码的参数值')
    ticket = models.CharField(max_length=20, verbose_name='二维码的ticket，可用来换取二维码图片')

    class Meta:
        ordering = ['-id']
        verbose_name_plural = verbose_name = u"用户上报地理位置事件"


class ClickEvent(models.Model):
    message = models.ForeignKey('Message', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="信息")
    menu = models.ForeignKey(MenuButton)
    event = models.CharField(max_length=20, choices=EVENT_TYPE)
    event_key = models.CharField(max_length=20, verbose_name='事件KEY值，qrscene_为前缀，后面为二维码的参数值')
    ticket = models.CharField(max_length=20, verbose_name='二维码的ticket，可用来换取二维码图片')

    class Meta:
        ordering = ['-id']
        verbose_name_plural = verbose_name = u"点击菜单拉取消息事件"


class ViewEvent(models.Model):
    message = models.ForeignKey('Message', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="信息")
    menu = models.ForeignKey(MenuButton)
    event = models.CharField(max_length=20, choices=EVENT_TYPE)
    event_key = models.CharField(max_length=20, verbose_name='事件KEY值，qrscene_为前缀，后面为二维码的参数值')
    ticket = models.CharField(max_length=20, verbose_name='二维码的ticket，可用来换取二维码图片')

    class Meta:
        ordering = ['-id']
        verbose_name_plural = verbose_name = u"点击菜单跳转链接事件"


class MassSendJobFinishEvent(models.Model):
    message = models.ForeignKey('Message', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="信息")
    menu = models.ForeignKey(MenuButton)
    event = models.CharField(max_length=20, choices=EVENT_TYPE)
    event_key = models.CharField(max_length=20, verbose_name='事件KEY值，qrscene_为前缀，后面为二维码的参数值')
    ticket = models.CharField(max_length=20, verbose_name='二维码的ticket，可用来换取二维码图片')

    class Meta:
        ordering = ['-id']
        verbose_name_plural = verbose_name = u"群发消息发送任务完成事件"


class TemplateSendJobFinishEvent(models.Model):
    message = models.ForeignKey('Message', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="信息")
    menu = models.ForeignKey(MenuButton)
    event = models.CharField(max_length=20, choices=EVENT_TYPE)
    event_key = models.CharField(max_length=20, verbose_name='事件KEY值，qrscene_为前缀，后面为二维码的参数值')
    ticket = models.CharField(max_length=20, verbose_name='二维码的ticket，可用来换取二维码图片')

    class Meta:
        ordering = ['-id']
        verbose_name_plural = verbose_name = u"模板消息发送任务完成事件"


class ScanCodePushEvent(models.Model):
    message = models.ForeignKey('Message', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="信息")
    menu = models.ForeignKey(MenuButton)
    event = models.CharField(max_length=20, choices=EVENT_TYPE)
    event_key = models.CharField(max_length=20, verbose_name='事件KEY值，qrscene_为前缀，后面为二维码的参数值')
    ticket = models.CharField(max_length=20, verbose_name='二维码的ticket，可用来换取二维码图片')

    class Meta:
        ordering = ['-id']
        verbose_name_plural = verbose_name = u"扫码推事件"


class PicPhotoOrAlbumEvent(models.Model):
    message = models.ForeignKey('Message', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="信息")
    menu = models.ForeignKey(MenuButton)
    event = models.CharField(max_length=20, choices=EVENT_TYPE)
    event_key = models.CharField(max_length=20, verbose_name='事件KEY值，qrscene_为前缀，后面为二维码的参数值')
    ticket = models.CharField(max_length=20, verbose_name='二维码的ticket，可用来换取二维码图片')

    class Meta:
        ordering = ['-id']
        verbose_name_plural = verbose_name = u"发图事件"


class LocationSelectEvent(models.Model):
    message = models.ForeignKey('Message', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="信息")
    menu = models.ForeignKey(MenuButton)
    event = models.CharField(max_length=20, choices=EVENT_TYPE)
    event_key = models.CharField(max_length=20, verbose_name='事件KEY值，qrscene_为前缀，后面为二维码的参数值')
    ticket = models.CharField(max_length=20, verbose_name='二维码的ticket，可用来换取二维码图片')

    class Meta:
        ordering = ['-id']
        verbose_name_plural = verbose_name = u"弹出地理位置选择器事件"
