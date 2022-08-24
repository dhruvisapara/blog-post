import django_filters
from django_filters import rest_framework as filters
from blog.models import Blog


class NameFilter(filters.FilterSet):
    class Meta:
        fields = ['name','user']
    title = filters.CharFilter(lookup_expr='icontains')
    user = filters.CharFilter(field_name='user__username', lookup_expr='icontains')


class DateFilter(filters.FilterSet):

    timestamp_gte = django_filters.DateTimeFilter(field_name="pub_date", lookup_expr='gte')
    timestamp_lte = django_filters.DateTimeFilter(field_name="pub_date", lookup_expr='lte')

    class Meta:
        model = Blog
        fields = ['timestamp_gte','timestamp_lte']


class Searchfilter(NameFilter,DateFilter):
    class Meta:
        model = Blog
        fields = ['title']

