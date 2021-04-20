import re

from django.shortcuts import render, HttpResponse, redirect
from .models import Users
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
            verify_account = Users.objects.filter(username=valid_result['username']).first()
            if verify_account:
                verify_password = Users.objects.filter(id=verify_account['id'],
                                                       password=valid_result['password']).first()
                if verify_password:
                    return redirect('/login/')
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
            print(valid_result)
            create_result = Users.objects.create(valid_result)
            print(create_result)
            msg = success(message='成功', data=valid_result)
        else:
            msg = unauth(message='失败', data=register_form.errors)
    return HttpResponse(msg)


def index(request):
    if request.method == 'GET':
        return render(request, 'index.html')
    else:
        pass
