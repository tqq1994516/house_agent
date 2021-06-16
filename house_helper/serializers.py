from rest_framework import serializers
from house_helper.models import User, Menus, BaseInfo, CallLog, TagType, Tag, TagRule, HouseInfo, TagRuleRelation, \
    TagRelation


class LoginSerializer(serializers.HyperlinkedModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'password')


class RegisterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = (
            'url', 'id', 'password', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'sex',
            'mobile_phone', 'birthday')


class MenusSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Menus
        fields = ('url', 'id', 'name', 'to_path', 'hierarchy', 'parent_id', 'have_child', 'icon', 'have_message_bubble')


class BaseInfoSerializer(serializers.HyperlinkedModelSerializer):
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
    class Meta:
        model = TagRelation
        fields = ('url', 'id', 'customer_name_id', 'tag_id')


class HouseInfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = HouseInfo
        fields = ('url', 'id', 'title', 'subhead', 'totalPrices', 'unitPrice', 'acreage', 'houseDoorModel', 'floor',
                  'familyStructure', 'insideSpace', 'buildingTypes', 'buildingStructure', 'buildingHead',
                  'decorateSituation', 'decorateSituation', 'haveElevator', 'propertyType', 'usageOfHouse',
                  'propertyOwnership', 'villageName', 'area', 'communityIsIntroduced', 'surroundingFacility',
                  'transportation', 'coreSellingPoint')
