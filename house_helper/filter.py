from django_filters import rest_framework as filters
from house_helper.models import base_info


class baseInfoFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')

    class Meta:
        model = base_info
        fields = ['category', 'in_stock']
