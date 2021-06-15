from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.core.cache import cache
from house_helper.admin import models


class LoginAuth(BaseAuthentication):
    def authenticate(self, request):
        token = request.GET.get("token")
        # 从Redis中取出token,前提是已经在settings中配置Redis
        user = cache.get(token)
        if user:
            return user, token
        # token = models.Token.objects.filter(key=token).first()
        # if token:
        #     return token.user, token
        else:
            raise AuthenticationFailed("尚未登陆")
