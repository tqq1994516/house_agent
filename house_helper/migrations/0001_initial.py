# Generated by Django 3.2.3 on 2021-06-16 17:52

import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('true_name', models.CharField(default='', max_length=128, verbose_name='姓名')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='邮箱')),
                ('sex', models.IntegerField(choices=[(1, '男'), (2, '女')], default=1, verbose_name='性别')),
                ('mobile_phone', models.BigIntegerField(unique=True, verbose_name='手机号')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='生日')),
                ('address', models.CharField(blank=True, max_length=128, null=True, verbose_name='住址')),
                ('c_time', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
                ('u_time', models.DateTimeField(auto_now_add=True, verbose_name='最后更新时间')),
            ],
            options={
                'verbose_name': '客户基础信息表',
                'verbose_name_plural': '客户基础信息表',
                'ordering': ['-c_time'],
            },
        ),
        migrations.CreateModel(
            name='HouseInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='标题')),
                ('subhead', models.CharField(max_length=150, verbose_name='副标题')),
                ('totalPrices', models.CharField(max_length=150, verbose_name='总价')),
                ('unitPrice', models.CharField(max_length=150, verbose_name='单价')),
                ('acreage', models.CharField(max_length=150, verbose_name='面积')),
                ('houseDoorModel', models.CharField(max_length=150, verbose_name='房屋户型')),
                ('floor', models.CharField(max_length=150, verbose_name='所在楼层')),
                ('familyStructure', models.CharField(max_length=150, verbose_name='户型结构')),
                ('insideSpace', models.CharField(max_length=150, verbose_name='套内面积')),
                ('buildingTypes', models.CharField(max_length=150, verbose_name='建筑类型')),
                ('buildingStructure', models.CharField(max_length=150, verbose_name='建筑结构')),
                ('buildingHead', models.CharField(max_length=150, verbose_name='房屋朝向')),
                ('decorateSituation', models.CharField(max_length=150, verbose_name='装修情况')),
                ('ladderHouseholdProportion', models.CharField(max_length=150, verbose_name='梯户比例')),
                ('haveElevator', models.CharField(max_length=150, verbose_name='是否用电梯')),
                ('propertyType', models.CharField(max_length=150, verbose_name='产权类型')),
                ('usageOfHouse', models.CharField(max_length=150, verbose_name='房屋用途')),
                ('propertyOwnership', models.CharField(max_length=150, verbose_name='产权所属')),
                ('villageName', models.CharField(max_length=150, verbose_name='小区名称')),
                ('area', models.CharField(max_length=150, verbose_name='所在地区')),
                ('communityIsIntroduced', models.CharField(max_length=150, verbose_name='小区介绍')),
                ('surroundingFacility', models.CharField(max_length=150, verbose_name='周边配套')),
                ('transportation', models.CharField(max_length=150, verbose_name='交通出现')),
                ('coreSellingPoint', models.CharField(max_length=150, verbose_name='核心卖点')),
                ('c_time', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
                ('u_time', models.DateTimeField(auto_now_add=True, verbose_name='最后更新时间')),
            ],
            options={
                'verbose_name': '房源信息表',
                'verbose_name_plural': '房源信息表',
                'ordering': ['-u_time'],
            },
        ),
        migrations.CreateModel(
            name='Menus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=128, unique=True, verbose_name='菜单名称')),
                ('to_path', models.CharField(default='#', max_length=128, verbose_name='跳转地址')),
                ('hierarchy', models.IntegerField(default=1, verbose_name='菜单层级')),
                ('parent_id', models.IntegerField(default=0, verbose_name='父级菜单id')),
                ('have_child', models.BooleanField(default=True, verbose_name='是否含有子菜单')),
                ('icon', models.CharField(blank=True, default='', max_length=128, null=True, verbose_name='菜单图标')),
                ('have_message_bubble', models.BooleanField(default=False, verbose_name='是否具有消息气泡')),
                ('c_time', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
                ('u_time', models.DateTimeField(auto_now_add=True, verbose_name='最后更新时间')),
            ],
            options={
                'verbose_name': '菜单列表',
                'verbose_name_plural': '菜单列表',
                'ordering': ['u_time'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='标签名称')),
                ('c_time', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
                ('u_time', models.DateTimeField(auto_now_add=True, verbose_name='最后更新时间')),
            ],
            options={
                'verbose_name': '标签列表',
                'verbose_name_plural': '标签列表',
                'ordering': ['-u_time'],
            },
        ),
        migrations.CreateModel(
            name='TagRule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rule_name', models.CharField(max_length=150, verbose_name='规则名称')),
                ('c_time', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
                ('u_time', models.DateTimeField(auto_now_add=True, verbose_name='最后更新时间')),
            ],
            options={
                'verbose_name': '标签规则表',
                'verbose_name_plural': '标签规则表',
                'ordering': ['-u_time'],
            },
        ),
        migrations.CreateModel(
            name='TagType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='标签类型')),
                ('c_time', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
                ('u_time', models.DateTimeField(auto_now_add=True, verbose_name='最后更新时间')),
            ],
            options={
                'verbose_name': '标签类型表',
                'verbose_name_plural': '标签类型表',
                'ordering': ['-u_time'],
            },
        ),
        migrations.CreateModel(
            name='TagRuleRelation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('c_time', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
                ('u_time', models.DateTimeField(auto_now_add=True, verbose_name='最后更新时间')),
                ('rule_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='house_helper.tagrule', verbose_name='规则id')),
                ('tag_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='house_helper.tag', verbose_name='标签id')),
            ],
            options={
                'verbose_name': '标签规则与标签关系表',
                'verbose_name_plural': '标签规则与标签关系表',
                'ordering': ['-u_time'],
            },
        ),
        migrations.CreateModel(
            name='TagRelation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('c_time', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
                ('u_time', models.DateTimeField(auto_now_add=True, verbose_name='最后更新时间')),
                ('customer_name_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='house_helper.baseinfo')),
                ('tag_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='house_helper.tag', verbose_name='标签id')),
            ],
            options={
                'verbose_name': '客户与标签关系表',
                'verbose_name_plural': '客户与标签关系表',
                'ordering': ['-u_time'],
            },
        ),
        migrations.AddField(
            model_name='tag',
            name='type_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='house_helper.tagtype'),
        ),
        migrations.CreateModel(
            name='CallLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(choices=[(1, '来电'), (2, '去电')], default=1, verbose_name='通话类型')),
                ('start_time', models.DateTimeField(verbose_name='开始时间')),
                ('end_time', models.DateTimeField(verbose_name='结束时间')),
                ('call_duration', models.IntegerField(verbose_name='通话时长')),
                ('c_time', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
                ('u_time', models.DateTimeField(auto_now_add=True, verbose_name='最后更新时间')),
                ('contacts_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='house_helper.baseinfo', verbose_name='联系人id')),
            ],
            options={
                'verbose_name': '通话记录表',
                'verbose_name_plural': '通话记录表',
                'ordering': ['-c_time'],
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='用户名')),
                ('email', models.EmailField(error_messages={'unique': 'A user with that email already exists.'}, max_length=254, unique=True, verbose_name='邮箱')),
                ('mobile_phone', models.CharField(error_messages={'unique': 'A user with that mobilePhone already exists.'}, max_length=11, unique=True, verbose_name='手机号')),
                ('first_name', models.CharField(blank=True, max_length=150, null=True, verbose_name='姓')),
                ('last_name', models.CharField(blank=True, max_length=150, null=True, verbose_name='名')),
                ('sex', models.IntegerField(choices=[(1, '男'), (2, '女')], default=1, error_messages={'required': '性别不能为空'}, verbose_name='性别')),
                ('birthday', models.DateField(default=django.utils.timezone.now, verbose_name='出生日期')),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='最后一次登录时间')),
                ('c_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('u_time', models.DateTimeField(auto_now=True, verbose_name='最后更新时间')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': '账户信息表',
                'verbose_name_plural': '账户信息表',
                'ordering': ['-c_time'],
            },
        ),
    ]
