import re

from django.contrib.auth.hashers import make_password, check_password, is_password_usable
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

GENDER = ((1, '男'), (2, '女'))


class UserInfo(models.Model):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(max_length=150,
                                unique=True,
                                help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
                                validators=[username_validator],
                                error_messages={
                                    'unique': "A user with that username already exists.",
                                }, verbose_name='用户名')
    password = models.CharField(max_length=150, verbose_name='密码')
    first_name = models.CharField(max_length=150, blank=True, verbose_name='姓')
    last_name = models.CharField(max_length=150, blank=True, verbose_name='名')
    email = models.EmailField(blank=True, verbose_name='邮箱')
    sex = models.IntegerField(choices=GENDER, default=1, verbose_name='性别', error_messages={'required': '性别不能为空'})
    mobile_phone = models.CharField(unique=True, max_length=11, verbose_name='手机号')
    is_staff = models.BooleanField(
        verbose_name='是否登录',
        default=False,
        help_text='Designates whether the user can log into this admin site.',
    )
    is_active = models.BooleanField(
        verbose_name='是否激活',
        default=True,
        help_text=
        'Designates whether this user should be treated as active. '
        'Unselect this instead of deleting accounts.'
        ,
    )
    birthday = models.DateField(default=timezone.now, verbose_name='出生日期')
    last_login = models.DateTimeField(blank=True, null=True, verbose_name='最后一次登录时间')
    c_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    u_time = models.DateTimeField(auto_now=True, verbose_name='最后更新时间')

    def validate_mobile_phone(self, exclude=None):
        if not re.match(r'^1[356789]\d{9}$', exclude):
            raise models.ValidationError('手机号码格式错误！！！')
        return exclude

    def __str__(self):
        return self.username

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self._password = raw_password

    def check_password(self, raw_password):
        """
        Return a boolean of whether the raw_password was correct. Handles
        hashing formats behind the scenes.
        """
        def setter(raw_password):
            self.set_password(raw_password)
            # Password hash upgrades shouldn't be considered password changes.
            self._password = None
            self.save(update_fields=["password"])
        return check_password(raw_password, self.password, setter)

    def set_unusable_password(self):
        # Set a value that will never be a valid hash
        self.password = make_password(None)

    def has_usable_password(self):
        """
        Return False if set_unusable_password() has been called for this user.
        """
        return is_password_usable(self.password)


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
    to_path = models.CharField(max_length=128, default='#', verbose_name='跳转地址')
    hierarchy = models.IntegerField(default=1, verbose_name='菜单层级')
    parent_id = models.IntegerField(default=0, verbose_name='父级菜单id')
    have_child = models.BooleanField(default=True, verbose_name='是否含有子菜单')
    icon = models.CharField(max_length=128, default='', null=True, blank=True, verbose_name='菜单图标')
    have_message_bubble = models.BooleanField(default=False, verbose_name='是否具有消息气泡')
    c_time = models.DateTimeField(auto_now=True, verbose_name='创建时间')
    u_time = models.DateTimeField(auto_now_add=True, verbose_name='最后更新时间')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['u_time']
        verbose_name = '菜单列表'
        verbose_name_plural = '菜单列表'
