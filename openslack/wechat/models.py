# -*- coding: utf-8 -*-
from django.db import models
import json,time
from utils.common import upload_file_handler, method_get_api, method_post_api
# Create your models here.

TYPE_LIST = (
    ('text', '文本回复'),
    ('news', '图文回复'),
    ('event', 'event'),
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

class Member(models.Model):
    name = models.CharField(max_length=200, verbose_name='姓名')
    avatar = models.CharField(max_length=200, verbose_name='头像')
    openid = models.CharField(max_length=200, verbose_name='微信ID')
    city = models.CharField(max_length=200, verbose_name='城市')
    created = models.DateTimeField(auto_now_add=True, verbose_name='注册时间')
    updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __unicode__(self):
        return self.name

    def avatar_url(self):
        return '<a href="%s" target="_blank"><img src="%s" height="50"></a>' % self.avatar

    class Meta(object):
        verbose_name = '会员'
        verbose_name_plural = '会员'

    avatar_url.allow_tag = True
    avatar_url.verbose_name='头像'


class Message(models.Model):
    type = models.CharField(max_length=100, blank=True, null=True, verbose_name='收到信息类型', choices=TYPE_LIST)
    keyword = models.CharField(max_length=100, blank=True, null=True, verbose_name='关键字')
    tag = models.CharField(max_length=100, default='keyword_recontent',verbose_name='标示', choices=MESSAGE_TAG)
    retype = models.CharField(max_length=100, verbose_name='返回信息类型', default='text',choices=RE_TYPE_LIST)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        ordering = ['-id']
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
        time_stamp=time.mktime(self.create_time.timetuple())
        return long(time_stamp)

    class Meta:
        ordering = ['-id']
        verbose_name_plural = verbose_name = u"Message"

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
    order_dic = models.CharField(max_length=512, blank=True, null=True, verbose_name='素材顺序') #"{art1.id:1, art2.id:2}"

    class Meta:
        ordering = ['-id']
        verbose_name_plural = verbose_name = u"News"

class Article(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True, verbose_name='标题')
    author = models.CharField(max_length=100, blank=True, null=True, verbose_name='作者')
    description = models.TextField(blank=True, null=True, verbose_name='描述')
    picurl = models.CharField(max_length=500, blank=True, null=True, verbose_name='图片链接')
    url = models.CharField(max_length=500, blank=True, null=True, verbose_name='原文链接')
    image = models.FileField(
        max_length=128, blank=True, null=True, upload_to=upload_file_handler, verbose_name="本地上传")
    content = models.TextField(blank=True, null=True, verbose_name='正文')
    create_time = models.DateTimeField(auto_now_add=True,  blank=True, null=True,verbose_name='创建时间')
    class Meta:
        verbose_name_plural=verbose_name = '素材'

        ordering = ['-id']

    def __unicode__(self):
        return self.title
    def get_appitem(self):
            return self.appitem_set.first()

    def get_image_url(self):
        if self.picurl:
            return self.picurl
        elif self.image:
            appitem = self.get_appitem()
            domain = appitem.domain
            url_prefix = 'http://%s/media/' % domain
            return url_prefix + self.image.name
        else:
            return '/'

    def get_url(self):
        appitem = self.get_appitem()

        return 'http://%s/a/%s/article-detail/%s/' % (appitem.domain, appitem.slug, self.id)

    def get_description(self):
        if self.description:
            return self.description
        else:
            return self.content[:15]

    def get_category(self):
        return self.category_set.first()

class Category(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name='名称')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    articles = models.ManyToManyField('Article', blank=True, null=True, verbose_name='素材')
    status = models.BooleanField(default=True, verbose_name="是否显示")
    class Meta:
        ordering = ['-id']
    def __unicode__(self):
        return self.name

    def get_url(self):
        appitem = self.appitem_set.first()
        user_info_url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid='+appitem.appid+'&redirect_uri=%s&response_type=code&scope=snsapi_base&state=STATE#wechat_redirect'
        url = 'http://%s/a/%s/articles-list/%s/' % (appitem.domain, appitem.slug, self.id)
        return user_info_url % url
        return url

    class Meta:
        verbose_name_plural=verbose_name = 'Category'

