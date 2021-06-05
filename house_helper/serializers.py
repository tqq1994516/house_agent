from rest_framework import serializers
from house_helper.models import UserInfo, Menus


class loginForm(serializers.HyperlinkedModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = UserInfo
        fields = ('url', 'id', 'username', 'password')


class menusSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Menus
        fields = ('url', 'id', 'name', 'to_path', 'hierarchy', 'parent_id', 'have_child', 'icon', 'have_message_bubble')


class registerForm(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserInfo
        fields = ('url', 'id', 'password', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'sex', 'mobile_phone', 'birthday')
