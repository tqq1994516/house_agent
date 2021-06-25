from django_filters import rest_framework as filters
from house_helper.models import BaseInfo, Gender, CallLog, CallType, TagType, Tag, HouseInfo, TagRule, TagRelation, \
    TagRuleRelation


class BaseInfoFilter(filters.FilterSet):
    sort = filters.OrderingFilter(fields=('id', 'true_name', 'email', 'mobile_phone', 'birthday', 'address'))
    sex = filters.ChoiceFilter(choices=Gender.choices)

    class Meta:
        model = BaseInfo
        fields = {
            'id': ['exact'],
            "true_name": ['exact', 'icontains'],
            'email': ['exact', 'icontains'],
            'mobile_phone': ['exact', 'icontains'],
            'birthday': ['gt', 'lt', 'gte', 'lte', 'exact', 'icontains', 'range'],
            'address': ['exact', 'icontains']
        }


class CallLogFilter(filters.FilterSet):
    sort = filters.OrderingFilter(
        fields=('id', 'type', 'contacts_id', 'contacts_id__true_name', 'start_time', 'end_time', 'call_duration'))
    type = filters.ChoiceFilter(choices=CallType.choices)

    class Meta:
        model = CallLog
        fields = {
            'id': ['exact'],
            'contacts_id__true_name': ['exact', 'icontains'],
            'start_time': ['gt', 'lt', 'gte', 'lte', 'exact', 'icontains', 'range'],
            'end_time': ['gt', 'lt', 'gte', 'lte', 'exact', 'icontains', 'range'],
            'call_duration': ['gt', 'lt', 'gte', 'lte', 'exact', 'icontains', 'range']
        }


class TagTypeFilter(filters.FilterSet):
    sort = filters.OrderingFilter(fields=('id', 'name'))

    class Meta:
        model = TagType
        fields = {
            'id': ['exact'],
            'name': ['exact', 'icontains']
        }


class TagFilter(filters.FilterSet):
    sort = filters.OrderingFilter(fields=('id', 'name', 'type_id__name', 'type_id'))

    class Meta:
        model = Tag
        fields = {
            'id': ['exact'],
            'name': ['exact', 'icontains'],
            'type_id__name': ['exact', 'icontains']
        }


class TagRuleFilter(filters.FilterSet):
    sort = filters.OrderingFilter(fields=('id', 'rule_name'))

    class Meta:
        model = TagRule
        fields = {
            'id': ['exact'],
            'rule_name': ['exact', 'icontains']
        }


class TagRuleRelationFilter(filters.FilterSet):
    sort = filters.OrderingFilter(fields=('id', 'rule_id', 'tag_id', 'rule_id__rule_name', 'tag_id__name'))

    class Meta:
        model = TagRuleRelation
        fields = {
            'id': ['exact'],
            'rule_id__rule_name': ['exact', 'icontains'],
            'tag_id__name': ['exact', 'icontains'],
        }


class TagRelationFilter(filters.FilterSet):
    sort = filters.OrderingFilter(
        fields=('id', 'customer_name_id', 'customer_name_id__true_name', 'tag_id__name', 'tag_id'))

    class Meta:
        model = TagRelation
        fields = {
            'id': ['exact'],
            'customer_name_id': ['exact'],
            'customer_name_id__true_name': ['exact', 'icontains'],
            'tag_id__name': ['exact', 'icontains'],
        }


class HouseInfoFilter(filters.FilterSet):
    sort = filters.OrderingFilter(
        fields=('id', 'title', 'subhead', 'totalPrices', 'unitPrice', 'acreage', 'houseDoorModel', 'floor',
                'familyStructure', 'insideSpace', 'buildingTypes', 'buildingStructure', 'buildingHead',
                'decorateSituation', 'haveElevator', 'propertyType', 'usageOfHouse',
                'propertyOwnership', 'villageName', 'area', 'communityIsIntroduced', 'surroundingFacility',
                'transportation', 'coreSellingPoint'))

    class Meta:
        model = HouseInfo
        fields = {
            'id': ['exact'],
            'title': ['exact', 'icontains'],
            'subhead': ['exact', 'icontains'],
            'totalPrices': ['exact', 'icontains', 'gt', 'lt', 'gte', 'lte', 'range'],
            'unitPrice': ['exact', 'icontains', 'gt', 'lt', 'gte', 'lte', 'range'],
            'acreage': ['exact', 'icontains', 'gt', 'lt', 'gte', 'lte', 'range'],
            'houseDoorModel': ['exact', 'icontains'],
            'floor': ['exact', 'icontains'],
            'familyStructure': ['exact', 'icontains'],
            'insideSpace': ['exact', 'icontains', 'gt', 'lt', 'gte', 'lte', 'range'],
            'buildingTypes': ['exact', 'icontains'],
            'buildingStructure': ['exact', 'icontains'],
            'buildingHead': ['exact', 'icontains'],
            'decorateSituation': ['exact', 'icontains'],
            'haveElevator': ['exact', 'icontains'],
            'propertyType': ['exact', 'icontains'],
            'usageOfHouse': ['exact', 'icontains'],
            'propertyOwnership': ['exact', 'icontains'],
            'villageName': ['exact', 'icontains'],
            'area': ['exact', 'icontains'],
            'communityIsIntroduced': ['exact', 'icontains'],
            'surroundingFacility': ['exact', 'icontains'],
            'transportation': ['exact', 'icontains'],
            'coreSellingPoint': ['exact', 'icontains'],
        }
