from django import forms
from house_helper.models import Users


class loginForm(forms.Form):
    username_label = '用户名'
    password_label = '密码'
    username = forms.CharField(label=username_label, max_length=30,
                               min_length=1, error_messages={'required': '用户名不能为空', 'min_length': '用户名最少为1个字符',
                                                             'max_length': '用户名最多为30个字符'},
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control', 'placeholder': username_label, 'autofocus': 'True'}))
    password = forms.CharField(label=password_label, max_length=30, min_length=1,
                               error_messages={'required': '密码不能为空', 'min_length': '密码最少为1个字符',
                                               'max_length': '密码最多为30个字符'}, widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': password_label}))


class registerForm(forms.Form):
    username_label = '用户名'
    password_label = '密码'
    password2_label = '确认密码'
    true_name_label = '姓名'
    email_label = '邮箱'
    sex_label = '性别'
    sex_choices = Users.GENDER
    mobile_phone_label = '手机'
    username = forms.CharField(label=username_label, max_length=30, min_length=1,
                               error_messages={'required': '用户名不能为空', 'min_length': '用户名最少为1个字符',
                                               'max_length': '用户名最多为30个字符'}, widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': username_label, 'autoFocus': 'True'}))
    password = forms.CharField(label=password_label, max_length=30, min_length=1,
                               error_messages={'required': '密码不能为空', 'min_length': '密码最少为1个字符',
                                               'max_length': '密码最多为30个字符'}, widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': password_label}))
    password2 = forms.CharField(label=password2_label, max_length=30, min_length=1,
                                error_messages={'required': '密码不能为空', 'min_length': '密码最少为1个字符',
                                                'max_length': '密码最多为30个字符'}, widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': password2_label}))
    true_name = forms.CharField(label=true_name_label, max_length=30, min_length=2,
                                error_messages={'required': '姓名不能为空', 'min_length': '姓名最少为2个字符',
                                                'max_length': '姓名最多为30个字符'}, widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': true_name_label}))
    email = forms.EmailField(label=email_label, required=False, widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': email_label}))
    sex = forms.ChoiceField(label=sex_label, error_messages={'required': '性别不能为空'}, choices=sex_choices,
                            widget=forms.RadioSelect())
    mobile_phone = forms.IntegerField(label=mobile_phone_label, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': mobile_phone_label}))
