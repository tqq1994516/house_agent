import re
import sys
from uuid import uuid4
from django.contrib import admin
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, HttpResponse, redirect
from ratelimit.decorators import ratelimit
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from house_agent.Authentication import LoginAuth
from .admin import models
from .menu_management import get_menu_list
from .models import Users, Menus
from .serializers import loginForm, registerForm
from .restful import success, params_error, server_error, unauth, method_error


class login(APIView):
    authentication_classes = []
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request):
        serializer = loginForm()
        return Response(serializer.data)

    def post(self, request):
        serializer = loginForm(request.POST)
        if serializer.is_valid():
            valid_result = serializer.save()
            if re.search('^\\d', valid_result['username']).group():
                verify_account = Users.objects.filter(mobile_phone=valid_result['username']).first()
            else:
                verify_account = Users.objects.filter(username=valid_result['username']).first()
            if verify_account:
                verify_password = Users.objects.filter(id=verify_account.id).first()
                if verify_password.password.__eq__(valid_result['password']):
                    token = uuid4()
                    models.Token.objects.update_or_create(user=verify_account, defaults={'key': token})
                    cache.set(token, verify_account)
                    msg = success(message='成功', data={'login': ['登录成功']})
                else:
                    msg = unauth(message='失败', data={'password': ['账号输入有误或密码错误']})
            else:
                msg = unauth(message='失败', data={'username': ['该账号未注册']})
        else:
            msg = unauth(message='失败', data=serializer.errors)
        return Response(msg)

# def login(request):
#     if request.method == 'GET':
#         login_form = loginForm()
#         return render(request, 'login.html', {'form': login_form})
#     else:
#         login_form = loginForm(request.POST)
#         if login_form.is_valid():
#             valid_result = login_form.clean()
#             if re.search('^\\d', valid_result['username']).group():
#                 verify_account = Users.objects.filter(mobile_phone=valid_result['username']).first()
#             else:
#                 verify_account = Users.objects.filter(username=valid_result['username']).first()
#             if verify_account:
#                 verify_password = Users.objects.filter(id=verify_account.id).first()
#                 if verify_password.password.__eq__(valid_result['password']):
#                     msg = success(message='成功', data={'login': ['登录成功']})
#                     # token = uuid4()
#                     # try:
#                     #     models.Token.objects.filter(key=token)
#                 else:
#                     msg = unauth(message='失败', data={'password': ['账号输入有误或密码错误']})
#             else:
#                 msg = unauth(message='失败', data={'username': ['该账号未注册']})
#         else:
#             msg = unauth(message='失败', data=login_form.errors)
#     return HttpResponse(msg)


def register(request):
    if request.method == 'GET':
        register_form = registerForm()
        # 利用正则找出django生成标签中choice的value，动态添加属性方式，将value值再加入到对应的choice中，模板中使用添加的属性名访问value
        for i, v in enumerate(register_form['sex']):
            step1 = re.search('value=\\"[0-9]*\\"', str(v)).group()
            step2 = re.search('\\d', step1).group()
            register_form['sex'][i].choice_value = step2
        return render(request, 'register.html', {'form': register_form})
    else:
        register_form = registerForm(request.POST)
        if register_form.is_valid():
            valid_result = register_form.clean()
            repeatability_verification_username = Users.objects.filter(username=valid_result['username']).first()
            repeatability_verification_email = Users.objects.filter(username=valid_result['email']).first()
            repeatability_verification_mobile_phone = Users.objects.filter(
                username=valid_result['mobile_phone']).first()
            if repeatability_verification_username:
                msg = params_error(message='失败', data={'username': ['账号已存在']})
            elif repeatability_verification_email:
                msg = params_error(message='失败', data={'email': ['邮箱已存在']})
            elif repeatability_verification_mobile_phone:
                msg = params_error(message='失败', data={'mobile_phone': ['手机号已存在']})
            elif re.search('^\\d', valid_result['username']):
                msg = params_error(message='失败', data={'username': ['账号不能以数字开头']})
            elif valid_result['password'] == valid_result['password2']:
                del valid_result['password2']
                try:
                    obj = Users.objects.create(**valid_result)
                    obj.save()
                except Exception:
                    msg = params_error(message='失败', data={'register': ['注册信息表内已存在']})
                    return HttpResponse(msg)
                msg = success(message='成功', data={'register': ['注册成功']})
            elif valid_result['password'] == valid_result['username']:
                msg = params_error(message='失败', data={'password': ['密码不能与账号一致']})
            else:
                msg = params_error(message='失败', data={'password2': ['两次密码不一致']})
        else:
            msg = unauth(message='失败', data=register_form.errors)
    return HttpResponse(msg)


def index(request):
    if request.method == 'GET':
        this_fun_name = sys._getframe().f_code.co_name
        menu_dict = get_menu_list(this_fun_name)
        return render(request, 'index.html', {'menu_list': menu_dict, 'username': request.user})


def crm(request):
    return redirect('base_info')


def base_info(request):
    if request.method == 'GET':
        this_fun_name = sys._getframe().f_code.co_name
        menu_dict = get_menu_list(this_fun_name)
        print(request.session)
        return render(request, 'base_info.html', {'menu_list': menu_dict, 'username': request.user})


def message(request):
    pass


# 覆盖默认的admin登录方法实现登录限流
@ratelimit(key='ip', rate='5/m', block=True)
def extend_admin_login(request, extra_context=None):
    return admin.site.login(request, extra_context)
