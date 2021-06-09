from rest_framework import serializers
from house_helper.models import UserInfo, Menus, base_info, call_log, tag_type, tag, tag_rule, house_info


class loginSerializer(serializers.HyperlinkedModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = UserInfo
        fields = ('url', 'id', 'username', 'password')


class menusSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Menus
        fields = ('url', 'id', 'name', 'to_path', 'hierarchy', 'parent_id', 'have_child', 'icon', 'have_message_bubble')


class registerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserInfo
        fields = (
        'url', 'id', 'password', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'sex',
        'mobile_phone', 'birthday')


class baseInfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = base_info
        fields = ('url', 'id', 'true_name', 'email', 'sex', 'mobile_phone', 'birthday', 'address')


class callLogSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = call_log
        fields = ('url', 'id', 'type', 'contacts_id', 'start_time', 'end_time', 'call_duration')


class tagTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = tag_type
        fields = ('url', 'id', 'name')


class tagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = tag
        fields = ('url', 'id', 'name', 'type')


class tagRuleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = tag_rule
        fields = ('url', 'id', 'rule_name')


class houseInfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = house_info
        fields = ('url', 'id', 'title', 'subhead', 'totalPrices', 'unitPrice', 'acreage', 'houseDoorModel', 'floor',
                  'familyStructure', 'insideSpace', 'buildingTypes', 'buildingStructure', 'buildingHead',
                  'decorateSituation', 'decorateSituation', 'haveElevator', 'propertyType', 'usageOfHouse',
                  'propertyOwnership', 'villageName', 'area', 'communityIsIntroduced', 'surroundingFacility',
                  'transportation', 'coreSellingPoint')
