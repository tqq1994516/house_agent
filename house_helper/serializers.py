from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from house_helper.models import User, Menus, BaseInfo, CallLog, TagType, Tag, TagRule, HouseInfo, TagRuleRelation, \
    TagRelation


class LoginSerializer(serializers.HyperlinkedModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'password')


class RegisterSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(label='Password')
    password2 = serializers.CharField(label='Password confirmation')
    sex = serializers.CharField(source='get_sex_display')

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'email', 'mobile_phone', 'first_name', 'last_name', 'sex', 'birthday', 'password' , 'password2')

    def create(self, validated_data):
        del validated_data['password2']
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    def clean_password2(self):
        # Check that the two password entries match
        password = self.validated_data.get("password")
        password2 = self.validated_data.get("password2")
        if password and password2 and password != password2:
            raise ValidationError("Passwords don't match")
        return password2


class UserChangeSerializer(serializers.HyperlinkedModelSerializer):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()
    sex = serializers.CharField(source='get_sex_display')

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'email', 'mobile_phone', 'password', 'first_name', 'last_name', 'sex', 'birthday', 'is_active', 'is_admin', 'is_superuser')


class MenusSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Menus
        fields = ('url', 'id', 'name', 'to_path', 'hierarchy', 'parent_id', 'have_child', 'icon', 'have_message_bubble')


class BaseInfoSerializer(serializers.HyperlinkedModelSerializer):
    sex = serializers.CharField(source='get_sex_display')

    class Meta:
        model = BaseInfo
        fields = ('url', 'id', 'true_name', 'email', 'sex', 'mobile_phone', 'birthday', 'address')


class CallLogSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CallLog
        fields = ('url', 'id', 'type', 'contacts_id', 'start_time', 'end_time', 'call_duration')


class TagTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TagType
        fields = ('url', 'id', 'name')


class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = ('url', 'id', 'name', 'type')


class TagRuleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TagRule
        fields = ('url', 'id', 'rule_name')


class TagRuleRelationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TagRuleRelation
        fields = ('url', 'id', 'rule_id', 'tag_id')


class TagRelationSerializer(serializers.HyperlinkedModelSerializer):
    customer_name_id = serializers.IntegerField(source='customer_name_id.id')
    true_name = serializers.CharField(source='customer_name_id.true_name')
    tag_name = serializers.CharField(source='tag_id.name')

    class Meta:
        model = TagRelation
        fields = ('url', 'id', 'customer_name_id', 'true_name', 'tag_name')


class HouseInfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = HouseInfo
        fields = ('url', 'id', 'title', 'subhead', 'totalPrices', 'unitPrice', 'acreage', 'houseDoorModel', 'floor',
                  'familyStructure', 'insideSpace', 'buildingTypes', 'buildingStructure', 'buildingHead',
                  'decorateSituation', 'decorateSituation', 'haveElevator', 'propertyType', 'usageOfHouse',
                  'propertyOwnership', 'villageName', 'area', 'communityIsIntroduced', 'surroundingFacility',
                  'transportation', 'coreSellingPoint')
