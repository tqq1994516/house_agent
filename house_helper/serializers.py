from rest_framework import serializers
from house_helper.models import Users
from house_helper import models


class loginForm(serializers.ModelSerializer):
    username_label = '用户名/手机号'
    password_label = '密码'
    username = serializers.CharField(label=username_label, max_length=30, min_length=1, style=({'input_type': 'text'}))
    password = serializers.CharField(label=password_label, max_length=30, min_length=1, style=({'input_type': 'password'}))

    class Meta:
        model = Users
        fields = ('username', 'password')


class registerForm(serializers.ModelSerializer):
    username_label = '用户名'
    password_label = '密码'
    password2_label = '确认密码'
    true_name_label = '姓名'
    email_label = '邮箱'
    sex_label = '性别'
    sex_choices = models.GENDER
    mobile_phone_label = '手机'
    username = serializers.CharField(label=username_label, max_length=30, min_length=1, style=({'input_type': 'text'}))
    password = serializers.CharField(label=password_label, max_length=30, min_length=1, style=({'input_tyoe': 'password'}))
    password2 = serializers.CharField(label=password2_label, max_length=30, min_length=1, style=({'input_tyoe': 'password'}))
    true_name = serializers.CharField(label=true_name_label, max_length=30, min_length=2, style=({'input_type': 'text'}))
    email = serializers.EmailField(label=email_label, required=False, style=({'input_type': 'text'}))
    sex = serializers.ChoiceField(label=sex_label, style=({'base_template': 'radio.html'}), choices=sex_choices)
    mobile_phone = serializers.IntegerField(label=mobile_phone_label, style=({'input_type': 'text'}))
