import re
import sys
from uuid import uuid4
from django.core.cache import cache
from django.db.models import Q
from django.shortcuts import render, HttpResponse, redirect
from rest_framework import permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from house_agent.MyCursorPagination import MyCursorPagination
from .admin import models
from .menu_management import get_menu_list
from .models import UserInfo, Menus
from .myResponse import myResponse
from .serializers import loginForm, registerForm, menusSerializer


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
                verify_account = UserInfo.objects.get(
                    Q(mobile_phone=valid_result['username']) | Q(username=valid_result['username']))
                if verify_account.check_passord(valid_result['password']):
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


class menuViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = []
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Menus.objects.all()
    serializer_class = menusSerializer

    @action(detail=False, methods=['get'])
    def menusList(self, request):
        activeIndex = request.query_params.get('activeIndex')
        data = self.get_queryset()
        # 进行分页处理
        # page = self.paginate_queryset(data)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True, context={'activeIndex': activeIndex})
        #     response = self.get_paginated_response(serializer.data)
        #     response.data['activeIndex'] = activeIndex
        #     return response
        serializer = self.get_serializer(data, many=True, context={'request': request})
        extra = {'activeIndex': activeIndex}
        response = myResponse(status.HTTP_200_OK, serializer.data, extra)
        return Response(response)


class registerViewSet(viewsets.ModelViewSet):
    authentication_classes = []
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = UserInfo.objects.all()
    serializer_class = registerForm
    ordering = 'c_time'

    def create(self, request, *args, **kwargs):
        pagination = MyCursorPagination()
        data = self.get_serializer(request.POST)
        if data.is_valid():
            valid_result = data.save()
            repeatability_verification_username = UserInfo.objects.filter(username=valid_result['username']).first()
            repeatability_verification_email = UserInfo.objects.filter(username=valid_result['email']).first()
            repeatability_verification_mobile_phone = UserInfo.objects.filter(
                username=valid_result['mobile_phone']).first()
            if repeatability_verification_username:
                response = myResponse(status.HTTP_400_BAD_REQUEST, data={'username': ['账号已存在']})
            elif repeatability_verification_email:
                response = myResponse(status.HTTP_400_BAD_REQUEST, data={'email': ['邮箱已存在']})
            elif repeatability_verification_mobile_phone:
                response = myResponse(status.HTTP_400_BAD_REQUEST, data={'mobile_phone': ['手机号已存在']})
            elif re.search('^\\d', valid_result['username']):
                response = myResponse(status.HTTP_400_BAD_REQUEST, data={'username': ['账号不能以数字开头']})
            elif valid_result['password'] == valid_result['password2']:
                del valid_result['password2']
                try:
                    obj = UserInfo.objects.create(**valid_result)
                    obj.save()
                except Exception:
                    response = myResponse(status.HTTP_400_BAD_REQUEST, data={'register': ['注册信息表内已存在']})
                    return Response(response)
                response = myResponse(status.HTTP_200_OK, data={'register': ['注册成功']})
            elif valid_result['password'] == valid_result['username']:
                response = myResponse(status.HTTP_400_BAD_REQUEST, data={'password': ['密码不能与账号一致']})
            else:
                response = myResponse(status.HTTP_400_BAD_REQUEST, data={'password2': ['两次密码不一致']})
        else:
            response = myResponse(status.HTTP_400_BAD_REQUEST, data=data.errors)
        return Response(response)


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
