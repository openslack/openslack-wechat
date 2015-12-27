# -*- coding: utf-8 -*-
from django.db import models
import json, time
from utils.common import upload_file_handler, method_get_api, method_post_api
"""
微信公众账号接收消息类，主要是用户发送的消息
"""

TYPE_LIST = (
    ('text', '文本回复'),
    ('image', '图片'),
    ('voice', '语音消息'),
    ('video', '视频'),
    ('location', '地理位置'),
    ('link', '链接'),
    ('shortvideo', '短视频'),
    ('news', '图文回复'),
    ('event', '事件'),
)
RE_TYPE_LIST = (
    ('text', '文本回复'),
    ('news', '图文回复'),
)

MESSAGE_TAG = (
    ('keyword_recontent', '关键字回复'),
    ('keyword_default_recontent', '无匹配回复'),
    ('subscribe', '关注'),
    # ('unsubscribe', '取消订阅')
)

MENU_BUTTON_CHOICES = (
    ('click', '关键字回复'),
    ('view', '跳转'),
    ('sub_button', '子按键'),
)

SUB_BUTTON_CHOICES = (
    ('click', '单击动作'),
    ('view', '跳转'),
)



class Message(models.Model):
    msg_id = models.IntegerField(default=0, verbose_name='信息id')
    source = models.CharField(max_length=100, default='', verbose_name='来源用户')
    target = models.CharField(max_length=100, default='', verbose_name='目标用户')
    type = models.CharField(max_length=100, blank=True, null=True, verbose_name='收到信息类型', choices=TYPE_LIST)
    keyword = models.CharField(max_length=100, blank=True, null=True, verbose_name='关键字')
    tag = models.CharField(max_length=100, default='keyword_recontent', verbose_name='标示', choices=MESSAGE_TAG)
    retype = models.CharField(max_length=100, verbose_name='返回信息类型', default='text', choices=RE_TYPE_LIST)
    signature = models.CharField(max_length=100, default='', verbose_name='签名')
    timestamp = models.IntegerField(default=0, verbose_name='时间')
    nonce = models.IntegerField(default=0, verbose_name='随机数字')
    echostr = models.IntegerField(default=0, verbose_name='校验数字')
    encrypt_type = models.CharField(max_length=100, default='aes', verbose_name='加密类型')
    msg_signature = models.CharField(max_length=100, default='', verbose_name='消息签名')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        ordering = ['-id']
        verbose_name_plural = verbose_name = u"Message"

    def __unicode__(self):
        return '%s__%s' % (self.keyword or 'default', self.tag)

    def get_resource(self):
        if self.retype == 'text':
            return self.text_set.first()
        elif self.retype == 'news':
            return self.news_set.first()

    def get_create_time(self):
        #   c_time = self.create_time
        #   to_zone = pytz.timezone(TIME_ZONE)
        #   local = c_time.astimezone(to_zone)
        #   return local.strftime("%Y%m%d%H%M")
        time_stamp = time.mktime(self.create_time.timetuple())
        return long(time_stamp)


class Text(models.Model):
    message = models.ForeignKey('Message', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="信息")
    content = models.TextField(blank=True, null=True, verbose_name='内容')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __unicode__(self):
        return self.content

    class Meta:
        ordering = ['-id']
        verbose_name_plural = verbose_name = u"Text"


class News(models.Model):
    messages = models.ManyToManyField('Message', blank=True, null=True, verbose_name="信息")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    articles = models.ManyToManyField('Article', blank=True, null=True, verbose_name='素材')
    order_dic = models.CharField(max_length=512, blank=True, null=True, verbose_name='素材顺序')  # "{art1.id:1, art2.id:2}"

    class Meta:
        ordering = ['-id']
        verbose_name_plural = verbose_name = u"News"


class Image(models.Model):
    messages = models.ManyToManyField('Message', blank=True, null=True, verbose_name="信息")
    url = models.URLField(u"图片地址")
    media_id = models.IntegerField(u"图片消息媒体id，可以调用多媒体文件下载接口拉取数据。")

    class Meta:
        ordering = ['-id']
        verbose_name_plural = verbose_name = u"图片消息"


class Voice(models.Model):
    messages = models.ManyToManyField('Message', blank=True, null=True, verbose_name="信息")
    media_id = models.IntegerField(u"微信内部的一个文件 ID")
    format = models.CharField(u"格式", max_length=50)
    recognition = models.CharField(u"语音识别结果", max_length=200, blank=True)

    class Meta:
        ordering = ['-id']
        verbose_name_plural = verbose_name = u"语音消息"


class Location(models.Model):
    messages = models.ManyToManyField('Message', blank=True, null=True, verbose_name="信息")
    location_y = models.FloatField("经度")
    location_x = models.FloatField("纬度")
    scale = models.IntegerField("地图缩放大小")
    label = models.CharField(u"地理位置信息", max_length=50)
    location = models.CharField(u"(纬度, 经度) 元组", max_length=50)

    class Meta:
        ordering = ['-id']
        verbose_name_plural = verbose_name = u"地理位置消息"


class Video(models.Model):
    messages = models.ManyToManyField('Message', blank=True, null=True, verbose_name="信息")
    media_id = models.IntegerField(u"微信内部的一个文件 ID")
    thumb_media_id = models.IntegerField(u"视频缩略图文件 ID")

    class Meta:
        ordering = ['-id']
        verbose_name_plural = verbose_name = u"视频消息"


class ShortVideo(models.Model):
    messages = models.ManyToManyField('Message', blank=True, null=True, verbose_name="信息")
    media_id = models.IntegerField(u"短视频 media_id")
    thumb_media_id = models.IntegerField(u"短视频缩略图 media_id")

    class Meta:
        ordering = ['-id']
        verbose_name_plural = verbose_name = u"短视频消息"


class Link(models.Model):
    messages = models.ManyToManyField('Message', blank=True, null=True, verbose_name="信息")
    title = models.CharField(u"	链接标题", max_length=200)
    description = models.TextField(u"链接描述")
    url = models.URLField(u"链接地址")

    class Meta:
        ordering = ['-id']
        verbose_name_plural = verbose_name = u"链接消息"




