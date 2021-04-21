import re
from django.core import serializers
from django.shortcuts import render, HttpResponse, redirect
from .models import Users, Menus
from .form import loginForm, registerForm
from .restful import success, params_error, server_error, unauth, method_error


# Create your views here.


def login(request):
    if request.method == 'GET':
        login_form = loginForm()
        return render(request, 'login.html', {'form': login_form})
    else:
        login_form = loginForm(request.POST)
        if login_form.is_valid():
            valid_result = login_form.clean()
            if re.search('^\\d', valid_result['username']).group():
                verify_account = Users.objects.filter(mobile_phone=valid_result['username']).first()
            else:
                verify_account = Users.objects.filter(username=valid_result['username']).first()
            if verify_account:
                verify_password = Users.objects.filter(id=verify_account.id).first()
                if verify_password.password.__eq__(valid_result['password']):
                    msg = success(message='成功', data={'login': ['登录成功']})
                else:
                    msg = unauth(message='失败', data={'password': ['账号输入有误或密码错误']})
            else:
                msg = unauth(message='失败', data={'username': ['该账号未注册']})
        else:
            msg = unauth(message='失败', data=login_form.errors)
    return HttpResponse(msg)


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
            repeatability_verification_mobile_phone = Users.objects.filter(username=valid_result['mobile_phone']).first()
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
        menu_list = Menus.objects.all()
        menu_dict = serializers.serialize("json", menu_list)
        return render(request, 'index.html', {'menu_list': menu_dict})
