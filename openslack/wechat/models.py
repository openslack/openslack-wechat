# -*- coding: utf-8 -*-
from django.db import models
import json, time
from utils.common import upload_file_handler, method_get_api, method_post_api
"""
微信公众账号本身类，包含素材。用户。菜单等基本的管理
"""

class MemberGroup(models.Model):
    name = models.CharField(max_length=200, verbose_name='姓名')
    created = models.DateTimeField(auto_now_add=True, verbose_name='注册时间')
    updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __unicode__(self):
        return self.name

    def avatar_url(self):
        return '<a href="%s" target="_blank"><img src="%s" height="50"></a>' % self.avatar

    class Meta(object):
        verbose_name = verbose_name_plural = '组'


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
    avatar_url.verbose_name = '头像'

    def followers(self, user_id=None):
        return client.user.get_followers(user_id)

    def group_id(self):
        return client.user.get_group_id(self.openid)

    def update_remark(self, remark):
        return client.user.update_remark(self.openid, remark)


class Article(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True, verbose_name='标题')
    author = models.CharField(max_length=100, blank=True, null=True, verbose_name='作者')
    description = models.TextField(blank=True, null=True, verbose_name='描述')
    picurl = models.CharField(max_length=500, blank=True, null=True, verbose_name='图片链接')
    url = models.CharField(max_length=500, blank=True, null=True, verbose_name='原文链接')
    image = models.FileField(
        max_length=128, blank=True, null=True, upload_to=upload_file_handler, verbose_name="本地上传")
    content = models.TextField(blank=True, null=True, verbose_name='正文')
    create_time = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name='创建时间')

    class Meta:
        verbose_name_plural = verbose_name = '素材'

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

    def send_message(self, user_id, content):
        client.message.send_text(user_id, content)

    def media(self):
        return client.media.xxx()


class Category(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name='名称')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    articles = models.ManyToManyField('Article', blank=True, null=True, verbose_name='素材')
    status = models.BooleanField(default=True, verbose_name="是否显示")

    class Meta:
        ordering = ['-id']
        verbose_name_plural = verbose_name = '分类'

    def __unicode__(self):
        return self.name

    def get_url(self):
        appitem = self.appitem_set.first()
        user_info_url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=' + appitem.appid + '&redirect_uri=%s&response_type=code&scope=snsapi_base&state=STATE#wechat_redirect'
        url = 'http://%s/a/%s/articles-list/%s/' % (appitem.domain, appitem.slug, self.id)
        # return user_info_url % url
        return url


class MenuButton(models.Model):
    type = models.CharField(max_length=100, default='click', verbose_name='标示', choices=MENU_BUTTON_CHOICES)
    name = models.CharField(max_length=128, blank=True, null=True, verbose_name='名称')
    key = models.CharField(max_length=128, blank=True, null=True, verbose_name='关键字')
    url = models.CharField(max_length=500, blank=True, null=True, verbose_name='跳转链接')
    sub_button = models.ManyToManyField('SubButton', blank=True, null=True, verbose_name='子按键')

    def __unicode__(self):
        return self.name

    def get_message(self):
        if self.type != 'click':
            return
        appitem = self.appitem_set.first()
        message = appitem.messages.filter(keyword=self.key, tag='keyword_recontent').first()
        return message

    def menus(self):
        return client.menu.get()


class SubButton(models.Model):
    type = models.CharField(max_length=100, default='click', verbose_name='标示', choices=SUB_BUTTON_CHOICES)
    name = models.CharField(max_length=128, blank=True, null=True, verbose_name='名称')
    key = models.CharField(max_length=128, blank=True, null=True, verbose_name='关键字')
    url = models.CharField(max_length=500, blank=True, null=True, verbose_name='跳转链接')

    def __unicode__(self):
        return self.name

    def get_message(self):
        if self.type != 'click':
            return
        menu_button = self.menubutton_set.first()
        appitem = menu_button.appitem_set.first()
        message = appitem.messages.filter(keyword=self.key, tag='keyword_recontent').first()
        return message


class QRCode(models.Model):
    scene_id = models.IntegerField(verbose_name="场景值ID", default=100, help_text="临时二维码时为32位非0整型，永久二维码时最大值为100000（目前参数只支持1--100000）")
    url = models.CharField(max_length=200, blank=True, null=True, verbose_name='资源链接')
    permanent = models.BooleanField(default=False, verbose_name="是否永久有效")
    action_name = models.CharField(max_length=100, verbose_name='二维码类型',help_text='QR_SCENE为临时,QR_LIMIT_SCENE为永久,QR_LIMIT_STR_SCENE为永久的字符串参数值')
    action_info = models.CharField(max_length=200, verbose_name='二维码详细信息')
    scene_str = models.CharField(max_length=100, verbose_name='场景值ID',help_text="场景值ID（字符串形式的ID），字符串类型，长度限制为1到64，仅永久二维码支持此字段")
    ticket = models.CharField(max_length=200, verbose_name='二维码ticket',help_text="获取的二维码ticket，凭借此ticket可以在有效时间内换取二维码。")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    expire_seconds = models.IntegerField(verbose_name="过期时间", default=0, blank=True, null=True)  # 0时永久有效
    message = models.ForeignKey('Message', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="处理事件")

    def create(self,qrcode_data):
        client.qrcode.create(data)

    def get_url(self,ticket):
        client.qrcode.get_url(ticket)

    def show(self,ticket):
        client.qrcode.show(ticket)

