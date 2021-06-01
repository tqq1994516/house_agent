from rest_framework import serializers
from house_helper.models import UserInfo, Menus


class loginForm(serializers.HyperlinkedModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = UserInfo
        fields = ('username', 'password')


class menusSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Menus
        fields = ('url', 'id', 'name', 'to_path', 'hierarchy', 'parent_id', 'have_child', 'icon', 'have_message_bubble')


class registerForm(serializers.HyperlinkedModelSerializer):
    password2_label = '确认密码'
    password2 = serializers.CharField(label=password2_label, max_length=30, min_length=1,
                                      style=({'base_template': 'input.html', 'input_type': 'password'}))

    class Meta:
        model = UserInfo
        fields = ('url', 'id', 'password', 'is_superuser', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'sex', 'mobile_phone')
