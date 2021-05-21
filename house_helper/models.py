import re

from django.db import models

# Create your models here.
GENDER = ((1, '男'), (2, '女'))


class Users(models.Model):
    username = models.CharField(max_length=128, unique=True, default='', verbose_name='用户名',
                                error_messages={'required': '用户名不能为空', 'min_length': '用户名最少为1个字符',
                                                'max_length': '用户名最多为30个字符'})
    password = models.CharField(max_length=128, default='', verbose_name='密码',
                                error_messages={'required': '密码不能为空', 'min_length': '密码最少为1个字符',
                                                'max_length': '密码最多为30个字符'})
    true_name = models.CharField(max_length=20, default='', verbose_name='姓名',
                                 error_messages={'required': '姓名不能为空', 'min_length': '姓名最少为2个字符',
                                                 'max_length': '姓名最多为30个字符'})
    email = models.EmailField(unique=True, default='', verbose_name='邮箱')
    sex = models.IntegerField(choices=GENDER, default=1, verbose_name='性别', error_messages={'required': '性别不能为空'})
    mobile_phone = models.BigIntegerField(unique=True, verbose_name='手机号')
    c_time = models.DateTimeField(auto_now=True, verbose_name='创建时间')
    u_time = models.DateTimeField(auto_now_add=True, verbose_name='最后更新时间')

    def validate_mobile_phone(self, exclude=None):
        if not re.match(r'^1[356789]\d{9}&', exclude):
            raise models.ValidationError('手机号码格式错误！！！')
        return exclude

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['-c_time']
        verbose_name = '账户信息表'
        verbose_name_plural = '账户信息表'


class base_info(models.Model):
    GENDER = ((1, '男'), (2, '女'))
    true_name = models.CharField(max_length=128, default='', verbose_name='姓名')
    email = models.EmailField(blank=True, null=True, verbose_name='邮箱')
    sex = models.IntegerField(choices=GENDER, default=1, verbose_name='性别')
    mobile_phone = models.BigIntegerField(unique=True, verbose_name='手机号')
    birthday = models.DateField(verbose_name='生日', null=True, blank=True)
    address = models.CharField(max_length=128, null=True, blank=True, verbose_name='住址')
    c_time = models.DateTimeField(auto_now=True, verbose_name='创建时间')
    u_time = models.DateTimeField(auto_now_add=True, verbose_name='最后更新时间')

    def __str__(self):
        return self.true_name

    class Meta:
        ordering = ['-c_time']
        verbose_name = '客户基础信息表'
        verbose_name_plural = '客户基础信息表'


class Menus(models.Model):
    name = models.CharField(max_length=128, unique=True, default='', verbose_name='菜单名称')
    en_name = models.CharField(max_length=128, unique=True, default='', verbose_name='英文名称')
    url = models.CharField(max_length=254, unique=True, default='', verbose_name='菜单地址')
    hierarchy = models.IntegerField(default=1, verbose_name='菜单层级')
    parent_id = models.IntegerField(default=0, verbose_name='父级菜单id')
    have_child = models.BooleanField(default=0, verbose_name='是否含有子菜单')
    icon = models.CharField(max_length=128, default='', verbose_name='菜单图标')
    have_message_bubble = models.BooleanField(default=0, verbose_name='是否具有消息气泡')
    c_time = models.DateTimeField(auto_now=True, verbose_name='创建时间')
    u_time = models.DateTimeField(auto_now_add=True, verbose_name='最后更新时间')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['u_time']
        verbose_name = '菜单列表'
        verbose_name_plural = '菜单列表'
