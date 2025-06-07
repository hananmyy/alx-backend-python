import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    sender = django_filters.CharFilter(field_name='sender__username', lookup_expr='iexact')
    date_range = django_filters.DateFromToRangeFilter(field_name='sent_at')

    class Meta:
        model = Message
        fields = ['sender', 'date_range']