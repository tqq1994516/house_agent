import re
from datetime import datetime
from uuid import uuid4
from django.core.cache import cache
from rest_framework import permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from .MyFilter import BaseInfoFilter, CallLogFilter, TagTypeFilter, TagFilter, TagRuleFilter, HouseInfoFilter, \
    TagRuleRelationFilter, TagRelationFilter
from .models import User, Menus, BaseInfo, CallLog, TagType, Tag, TagRule, HouseInfo, TagRuleRelation, TagRelation
from .myResponse import myResponse
from .serializers import LoginSerializer, MenusSerializer, BaseInfoSerializer, CallLogSerializer, \
    TagTypeSerializer, TagSerializer, TagRuleSerializer, HouseInfoSerializer, TagRuleRelationSerializer, \
    TagRelationSerializer, RegisterSerializer
from django.contrib.auth import authenticate, login, logout


class Login(APIView):
    authentication_classes = []
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        serializer = LoginSerializer()
        return Response(serializer.data)

    def post(self, request):
        data = LoginSerializer(data=request.data)
        if data.is_valid():
            valid_data = data.validated_data
            try:
                if re.search('[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$', valid_data['username']):
                    result_data = User.objects.filter(email=valid_data['username']).first()
                    if result_data:
                        valid_data['username'] = result_data.username
                    else:
                        response = myResponse(data={'message': '邮箱未注册', 'form': valid_data})
                        return Response(response, status=status.HTTP_400_BAD_REQUEST)
                elif re.search('^\\d', valid_data['username']):
                    result_data = User.objects.filter(mobile_phone=valid_data['username']).first()
                    if result_data:
                        valid_data['username'] = result_data.username
                    else:
                        response = myResponse(data={'message': '手机号未注册', 'form': valid_data})
                        return Response(response, status=status.HTTP_400_BAD_REQUEST)
                username = valid_data['username']
                password = valid_data['password']
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    token = uuid4()
                    cache.set(token, user)
                    response = myResponse(data={'message': '登录成功'})
                    headers = {authenticate: token}
                    return Response(response, status=status.HTTP_200_OK, headers=headers)
                else:
                    response = myResponse(data={'message': '账号输入有误或密码错误', 'form': valid_data})
                    return Response(response, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                print(e)
                response = myResponse(data={'message': '该账号未注册', 'form': valid_data})
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)


class Logout(APIView):
    authentication_classes = []
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        logout(request)
        token = request.headers['authenticate']
        cache.delete(token)
        response = myResponse(data={'message': '退出成果'})
        return Response(response, status=status.HTTP_200_OK)


class Register(APIView):
    authentication_classes = []
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        serializer = RegisterSerializer()
        return Response(serializer.data)

    def post(self, request):
        data = RegisterSerializer(data=request.data)
        if data.is_valid():
            valid_data = data.validated_data
            repeatability_verification_username = User.objects.filter(username=valid_data['username']).first()
            repeatability_verification_email = User.objects.filter(email=valid_data['email']).first()
            repeatability_verification_mobile_phone = User.objects.filter(
                mobile_phone=valid_data['mobile_phone']).first()
            if repeatability_verification_username:
                response = myResponse(data={'message': '账号已存在', 'form': valid_data})
            elif repeatability_verification_email:
                response = myResponse(data={'message': '邮箱已存在', 'form': valid_data})
            elif repeatability_verification_mobile_phone:
                response = myResponse(data={'message': '手机号已存在', 'form': valid_data})
            elif re.search('^\\d', valid_data['username']):
                response = myResponse(data={'message': '账号不能以数字开头', 'form': valid_data})
            elif valid_data['password'] == valid_data['username']:
                response = myResponse(data={'message': '密码不能与账号一致', 'form': valid_data})
            else:
                try:
                    data.save()
                    response = myResponse(data={'message': '注册成功'})
                    return Response(response, status=status.HTTP_200_OK)
                except Exception:
                    response = myResponse(data={'message': '注册信息表内已存在', 'form': valid_data})
                    return Response(response, status=status.HTTP_400_BAD_REQUEST)
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)


class MenuViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Menus.objects.all()
    serializer_class = MenusSerializer

    @action(detail=False, methods=['get'])
    def menusList(self, request):
        data = self.get_queryset()
        # 进行分页处理
        # page = self.paginate_queryset(data)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True, context={'activeIndex': activeIndex})
        #     response = self.get_paginated_response(serializer.data)
        #     response.data['activeIndex'] = activeIndex
        #     return response
        serializer = self.get_serializer(data, many=True, context={'request': request})
        response = myResponse(serializer.data)
        return Response(response, status=status.HTTP_200_OK)


class BaseInfoViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = BaseInfo.objects.all()
    serializer_class = BaseInfoSerializer
    filterset_class = BaseInfoFilter


class CallLogViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = CallLog.objects.all()
    serializer_class = CallLogSerializer
    filterset_class = CallLogFilter

    def calculate_call_duration(self, request, start_time=None, end_time=None):
        if start_time:
            start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        else:
            start_time = datetime.strptime(request.data['start_time'], "%Y-%m-%d %H:%M:%S")
        if end_time:
            end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
        else:
            end_time = datetime.strptime(request.data['end_time'], "%Y-%m-%d %H:%M:%S")
        request.data['call_duration'] = (end_time - start_time).total_seconds()

    def create(self, request, *args, **kwargs):
        self.calculate_call_duration(request)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        self.calculate_call_duration(request)
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        self.calculate_call_duration(request)
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class TagTypeViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = TagType.objects.all()
    serializer_class = TagTypeSerializer
    filterset_class = TagTypeFilter


class TagViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filterset_class = TagFilter


class TagRuleViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = TagRule.objects.all()
    serializer_class = TagRuleSerializer
    filterset_class = TagRuleFilter


class TagRuleRelationViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = TagRuleRelation.objects.all()
    serializer_class = TagRuleRelationSerializer
    filterset_class = TagRuleRelationFilter


class TagRelationViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = TagRelation.objects.all()
    serializer_class = TagRelationSerializer
    filterset_class = TagRelationFilter


class HouseInfoViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = HouseInfo.objects.all()
    serializer_class = HouseInfoSerializer
    filterset_class = HouseInfoFilter
