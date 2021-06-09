import re
from uuid import uuid4
from django.core.cache import cache
from rest_framework import permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from .menu_management import get_menu_list
from .models import UserInfo, Menus
from .myResponse import myResponse
from .serializers import loginForm, registerForm, menusSerializer


class login(APIView):
    authentication_classes = []
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        serializer = loginForm()
        return Response(serializer.data)

    def post(self, request):
        data = loginForm(data=request.data)
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


class logout(APIView):
    authentication_classes = []
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        pass


class register(APIView):
    authentication_classes = []
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        serializer = registerForm()
        return Response(serializer.data)

    def post(self, request):
        data = registerForm(data=request.data)
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
        response = myResponse(serializer.data, extra)
        return Response(response, status=status.HTTP_200_OK)

# def index(request):
#     if request.method == 'GET':
#         this_fun_name = sys._getframe().f_code.co_name
#         menu_dict = get_menu_list(this_fun_name)
#         return render(request, 'index.html', {'menu_list': menu_dict, 'username': request.user})


# def base_info(request):
#     if request.method == 'GET':
#         this_fun_name = sys._getframe().f_code.co_name
#         menu_dict = get_menu_list(this_fun_name)
#         print(request.session)
#         return render(request, 'base_info.html', {'menu_list': menu_dict, 'username': request.user})
