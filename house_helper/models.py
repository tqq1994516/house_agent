import re
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.exceptions import ValidationError


# Create your models here.
class Gender(models.IntegerChoices):
    MALE = (1, '男')
    FEMALE = (2, '女')


class CallType(models.IntegerChoices):
    DIAL_IN = (1, '来电')
    DIAL_OUT = (2, '去电')


class MyUserManager(BaseUserManager):
    def create_user(self, username, email, mobile_phone, password, first_name=None, last_name=None, sex=None,
                    birthday=None):
        if not username:
            raise ValueError('Users must have a username')
        if not email:
            raise ValueError('Users must have an email address')
        if not mobile_phone:
            raise ValueError('Users must have a mobilePhone')
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            mobile_phone=mobile_phone,
            first_name=first_name,
            last_name=last_name,
            sex=sex,
            birthday=birthday
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, mobile_phone, password, first_name=None, last_name=None, sex=None,
                         birthday=None):
        if not username:
            raise ValueError('Users must have a username')
        if not email:
            raise ValueError('Users must have an email address')
        if not mobile_phone:
            raise ValueError('Users must have a mobilePhone')
        user = self.create_user(
            username=username,
            email=email,
            mobile_phone=mobile_phone,
            password=password,
            first_name=first_name,
            last_name=last_name,
            sex=sex,
            birthday=birthday
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(max_length=150,
                                unique=True,
                                help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
                                validators=[username_validator],
                                error_messages={
                                    'unique': "A user with that username already exists.",
                                }, verbose_name='用户名')
    email = models.EmailField(unique=True, verbose_name='邮箱',
                              error_messages={'unique': 'A user with that email already exists.'})
    mobile_phone = models.CharField(unique=True, max_length=11, verbose_name='手机号',
                                    error_messages={'unique': 'A user with that mobilePhone already exists.'})
    first_name = models.CharField(max_length=150, null=True, blank=True, verbose_name='姓')
    last_name = models.CharField(max_length=150, null=True, blank=True, verbose_name='名')
    sex = models.IntegerField(choices=Gender.choices, null=True, blank=True, default=1, verbose_name='性别',
                              error_messages={'required': '性别不能为空'})
    birthday = models.DateField(null=True, blank=True, default=timezone.now, verbose_name='出生日期')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(blank=True, null=True, verbose_name='最后一次登录时间')
    c_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    u_time = models.DateTimeField(auto_now=True, verbose_name='最后更新时间')
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['mobile_phone', 'email']

    def validate_mobile_phone(self, exclude=None):
        if not re.match(r'^1[356789]\d{9}$', exclude):
            raise ValidationError('手机号码格式错误！！！')
        return exclude

    objects = MyUserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    class Meta:
        ordering = ['-c_time']
        verbose_name = '账户信息表'
        verbose_name_plural = '账户信息表'


class Menus(models.Model):
    name = models.CharField(max_length=128, unique=True, default='', verbose_name='菜单名称')
    to_path = models.CharField(max_length=128, default='#', verbose_name='跳转地址')
    hierarchy = models.IntegerField(default=1, verbose_name='菜单层级')
    parent_id = models.IntegerField(default=0, verbose_name='父级菜单id')
    have_child = models.BooleanField(default=True, verbose_name='是否含有子菜单')
    icon = models.CharField(max_length=128, default='', null=True, blank=True, verbose_name='菜单图标')
    have_message_bubble = models.BooleanField(default=False, verbose_name='是否具有消息气泡')
    c_time = models.DateTimeField(auto_now=True, verbose_name='创建时间')
    u_time = models.DateTimeField(auto_now_add=True, verbose_name='最后更新时间')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['u_time']
        verbose_name = '菜单列表'
        verbose_name_plural = '菜单列表'


class BaseInfo(models.Model):
    true_name = models.CharField(max_length=128, default='', verbose_name='姓名')
    email = models.EmailField(blank=True, null=True, verbose_name='邮箱')
    sex = models.IntegerField(choices=Gender.choices, default=1, verbose_name='性别')
    mobile_phone = models.BigIntegerField(unique=True, verbose_name='手机号')
    birthday = models.DateField(verbose_name='生日', null=True, blank=True)
    address = models.CharField(max_length=128, null=True, blank=True, verbose_name='住址')
    c_time = models.DateTimeField(auto_now=True, verbose_name='创建时间')
    u_time = models.DateTimeField(auto_now_add=True, verbose_name='最后更新时间')

    def __str__(self):
        return self.true_name

    def validate_mobile_phone(self, exclude=None):
        if not re.match(r'^1[356789]\d{9}$', exclude):
            raise models.ValidationError('手机号码格式错误！！！')
        return exclude

    class Meta:
        ordering = ['-c_time']
        verbose_name = '客户基础信息表'
        verbose_name_plural = '客户基础信息表'


class CallLog(models.Model):
    type = models.IntegerField(choices=CallType.choices, default=1, verbose_name='通话类型')
    contacts_id = models.ForeignKey(BaseInfo, on_delete=models.CASCADE, verbose_name='联系人id')  # 通过外键id查询对应名称
    start_time = models.DateTimeField(verbose_name='开始时间')
    end_time = models.DateTimeField(verbose_name='结束时间')
    call_duration = models.IntegerField(verbose_name='通话时长')
    c_time = models.DateTimeField(auto_now=True, verbose_name='创建时间')
    u_time = models.DateTimeField(auto_now_add=True, verbose_name='最后更新时间')

    class Meta:
        ordering = ['-c_time']
        verbose_name = '通话记录表'
        verbose_name_plural = '通话记录表'


class TagType(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='标签类型')
    c_time = models.DateTimeField(auto_now=True, verbose_name='创建时间')
    u_time = models.DateTimeField(auto_now_add=True, verbose_name='最后更新时间')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-u_time']
        verbose_name = '标签类型表'
        verbose_name_plural = '标签类型表'


class Tag(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='标签名称')
    type_id = models.ForeignKey(TagType, on_delete=models.CASCADE)
    c_time = models.DateTimeField(auto_now=True, verbose_name='创建时间')
    u_time = models.DateTimeField(auto_now_add=True, verbose_name='最后更新时间')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-u_time']
        verbose_name = '标签列表'
        verbose_name_plural = '标签列表'


class TagRule(models.Model):
    rule_name = models.CharField(max_length=150, verbose_name='规则名称')
    c_time = models.DateTimeField(auto_now=True, verbose_name='创建时间')
    u_time = models.DateTimeField(auto_now_add=True, verbose_name='最后更新时间')

    def __str__(self):
        return self.rule_name

    class Meta:
        ordering = ['-u_time']
        verbose_name = '标签规则表'
        verbose_name_plural = '标签规则表'


class TagRuleRelation(models.Model):
    rule_id = models.ForeignKey(TagRule, on_delete=models.CASCADE, verbose_name='规则id')
    tag_id = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name='标签id')
    c_time = models.DateTimeField(auto_now=True, verbose_name='创建时间')
    u_time = models.DateTimeField(auto_now_add=True, verbose_name='最后更新时间')

    class Meta:
        ordering = ['-u_time']
        verbose_name = '标签规则与标签关系表'
        verbose_name_plural = '标签规则与标签关系表'


class TagRelation(models.Model):
    customer_name_id = models.ForeignKey(BaseInfo, on_delete=models.CASCADE, verbose_name='客户id')
    tag_id = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name='标签id')
    c_time = models.DateTimeField(auto_now=True, verbose_name='创建时间')
    u_time = models.DateTimeField(auto_now_add=True, verbose_name='最后更新时间')

    class Meta:
        ordering = ['-u_time']
        verbose_name = '客户与标签关系表'
        verbose_name_plural = '客户与标签关系表'


class HouseInfo(models.Model):
    title = models.CharField(max_length=150, verbose_name='标题')
    subhead = models.CharField(max_length=150, verbose_name='副标题')
    totalPrices = models.CharField(max_length=150, verbose_name='总价')
    unitPrice = models.CharField(max_length=150, verbose_name='单价')
    acreage = models.CharField(max_length=150, verbose_name='面积')
    houseDoorModel = models.CharField(max_length=150, verbose_name='房屋户型')
    floor = models.CharField(max_length=150, verbose_name='所在楼层')
    familyStructure = models.CharField(max_length=150, verbose_name='户型结构')
    insideSpace = models.CharField(max_length=150, verbose_name='套内面积')
    buildingTypes = models.CharField(max_length=150, verbose_name='建筑类型')
    buildingStructure = models.CharField(max_length=150, verbose_name='建筑结构')
    buildingHead = models.CharField(max_length=150, verbose_name='房屋朝向')
    decorateSituation = models.CharField(max_length=150, verbose_name='装修情况')
    ladderHouseholdProportion = models.CharField(max_length=150, verbose_name='梯户比例')
    haveElevator = models.CharField(max_length=150, verbose_name='是否用电梯')
    propertyType = models.CharField(max_length=150, verbose_name='产权类型')
    usageOfHouse = models.CharField(max_length=150, verbose_name='房屋用途')
    propertyOwnership = models.CharField(max_length=150, verbose_name='产权所属')
    villageName = models.CharField(max_length=150, verbose_name='小区名称')
    area = models.CharField(max_length=150, verbose_name='所在地区')
    communityIsIntroduced = models.CharField(max_length=150, verbose_name='小区介绍')
    surroundingFacility = models.CharField(max_length=150, verbose_name='周边配套')
    transportation = models.CharField(max_length=150, verbose_name='交通出现')
    coreSellingPoint = models.CharField(max_length=150, verbose_name='核心卖点')
    c_time = models.DateTimeField(auto_now=True, verbose_name='创建时间')
    u_time = models.DateTimeField(auto_now_add=True, verbose_name='最后更新时间')

    class Meta:
        ordering = ['-u_time']
        verbose_name = '房源信息表'
        verbose_name_plural = '房源信息表'
