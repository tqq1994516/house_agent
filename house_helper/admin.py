from django.contrib import admin
from django.apps import apps
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from house_helper.models import User
from django.core.exceptions import ValidationError

# Register your models here.
# 自动注册所有model
models = apps.get_models()
for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'mobile_phone', 'first_name', 'last_name', 'sex', 'birthday')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('username', 'email', 'mobile_phone', 'password', 'first_name', 'last_name', 'sex', 'birthday', 'is_active', 'is_admin', 'is_superuser')


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username', 'email', 'mobile_phone', 'first_name', 'last_name', 'sex', 'birthday', 'is_admin', 'is_active', 'is_superuser')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('username', 'mobile_phone', 'email', 'password')}),
        ('Personal info', {'fields': ('birthday', 'first_name', 'last_name', 'sex')}),
        ('Permissions', {'fields': ('is_admin', 'is_active', 'is_superuser')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'mobile_phone', 'email', 'birthday', 'first_name', 'last_name', 'sex', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'username', 'mobile_phone', 'first_name', 'last_name')
    ordering = ('email', 'username', 'mobile_phone', 'birthday', 'first_name', 'last_name', 'sex')
    filter_horizontal = ()
