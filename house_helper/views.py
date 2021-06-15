import re
from datetime import datetime
from uuid import uuid4
from django.core.cache import cache
from rest_framework import permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from house_agent.MyCursorPagination import MyCursorPagination
from .filter import BaseInfoFilter, CallLogFilter, TagTypeFilter, TagFilter, TagRuleFilter, HouseInfoFilter, \
    TagRuleRelationFilter, TagRelationFilter
from .menu_management import get_menu_list
from .models import UserInfo, Menus, BaseInfo, CallLog, TagType, Tag, TagRule, HouseInfo, TagRuleRelation, TagRelation
from .myResponse import myResponse
from .serializers import LoginSerializer, RegisterSerializer, MenusSerializer, BaseInfoSerializer, CallLogSerializer, \
    TagTypeSerializer, TagSerializer, TagRuleSerializer, HouseInfoSerializer, TagRuleRelationSerializer, \
    TagRelationSerializer


class Login(APIView):
    authentication_classes = []
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        serializer = LoginSerializer()
        return Response(serializer.data)

    def post(self, request):
        data = LoginSerializer(data=request.data)
        if data.is_valid():
            try:
                if re.search('^\\d', request.data.get('username')).group():
                    userInfo = UserInfo.objects.get(mobile_phone=request.data.get('username')).first()
                else:
                    userInfo = UserInfo.objects.get(username=request.data.get('username')).first()
                if userInfo['password'] == request.data.get('password') and userInfo['is_staff'] == 2 and userInfo[
                    'is_active'] == 1:
                    token = uuid4()
                    cache.set(token, userInfo)
                    UserInfo.objects.filter(id=userInfo['id']).update(is_active='1')
                    response = myResponse(data={'message': '登录成功'})
                    return Response(response, status=status.HTTP_200_OK)
                else:
                    response = myResponse(data={'message': '账号输入有误或密码错误', 'form': data})
                    return Response(response, status=status.HTTP_400_BAD_REQUEST)
            except Exception:
                response = myResponse(data={'message': '该账号未注册', 'form': data})
                return Response(response, status=status.HTTP_400_BAD_REQUEST)


class Logout(APIView):
    authentication_classes = []
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        pass


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
            repeatability_verification_username = UserInfo.objects.filter(username=valid_data['username']).first()
            repeatability_verification_email = UserInfo.objects.filter(email=valid_data['email']).first()
            repeatability_verification_mobile_phone = UserInfo.objects.filter(
                mobile_phone=valid_data['mobile_phone']).first()
            if repeatability_verification_username:
                response = myResponse(data={'message': '账号已存在', 'form': data})
            elif repeatability_verification_email:
                response = myResponse(data={'message': '邮箱已存在', 'form': data})
            elif repeatability_verification_mobile_phone:
                response = myResponse(data={'message': '手机号已存在', 'form': data})
            elif re.search('^\\d', valid_data['username']):
                response = myResponse(data={'message': '账号不能以数字开头', 'form': data})
            elif valid_data['password'] == valid_data['username']:
                response = myResponse(data={'message': '密码不能与账号一致', 'form': data})
            else:
                try:
                    data.save()
                    response = myResponse(data={'message': '注册成功'})
                    return Response(response, status=status.HTTP_200_OK)
                except Exception as e:
                    print(Exception, e)
                    response = myResponse(data={'message': '注册信息表内已存在', 'form': data})
                    return Response(response, status=status.HTTP_400_BAD_REQUEST)
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)


class MenuViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = []
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Menus.objects.all()
    serializer_class = MenusSerializer

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
        response = myResponse(serializer.data, extra)
        return Response(response, status=status.HTTP_200_OK)


class BaseInfoViewSet(viewsets.ModelViewSet):
    authentication_classes = []
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = BaseInfo.objects.all()
    serializer_class = BaseInfoSerializer
    pagination_class = MyCursorPagination
    filterset_class = BaseInfoFilter


class CallLogViewSet(viewsets.ModelViewSet):
    authentication_classes = []
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = CallLog.objects.all()
    serializer_class = CallLogSerializer
    pagination_class = MyCursorPagination
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
    authentication_classes = []
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = TagType.objects.all()
    serializer_class = TagTypeSerializer
    pagination_class = MyCursorPagination
    filterset_class = TagTypeFilter


class TagViewSet(viewsets.ModelViewSet):
    authentication_classes = []
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = MyCursorPagination
    filterset_class = TagFilter


class TagRuleViewSet(viewsets.ModelViewSet):
    authentication_classes = []
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = TagRule.objects.all()
    serializer_class = TagRuleSerializer
    pagination_class = MyCursorPagination
    filterset_class = TagRuleFilter


class TagRuleRelationViewSet(viewsets.ModelViewSet):
    authentication_classes = []
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = TagRuleRelation.objects.all()
    serializer_class = TagRuleRelationSerializer
    pagination_class = MyCursorPagination
    filterset_class = TagRuleRelationFilter


class TagRelationViewSet(viewsets.ModelViewSet):
    authentication_classes = []
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = TagRelation.objects.all()
    serializer_class = TagRelationSerializer
    pagination_class = MyCursorPagination
    filterset_class = TagRelationFilter


class HouseInfoViewSet(viewsets.ModelViewSet):
    authentication_classes = []
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = HouseInfo.objects.all()
    serializer_class = HouseInfoSerializer
    pagination_class = MyCursorPagination
    filterset_class = HouseInfoFilter
