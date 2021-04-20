from django.db import models
from django import forms


# Create your models here.


class Users(models.Model):
    GENDER = ((1, '男'), (2, '女'))
    username = models.CharField(max_length=128, unique=True, null=True, blank=True, verbose_name='用户名')
    password = models.CharField(max_length=128, null=True, blank=True, verbose_name='密码')
    true_name = models.CharField(max_length=20, null=True, blank=True, verbose_name='姓名')
    email = models.EmailField(unique=True, verbose_name='邮箱')
    sex = models.IntegerField(choices=GENDER, default=1, verbose_name='性别')
    mobile_phone = models.IntegerField(unique=True, null=True, blank=True, verbose_name='手机号')
    u_time = models.DateTimeField(auto_now=True, verbose_name='创建时间')
    c_time = models.DateTimeField(auto_now_add=True, verbose_name='最后更新时间')

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['-c_time']
        verbose_name = '账户信息表'
        verbose_name_plural = '账户信息表'
