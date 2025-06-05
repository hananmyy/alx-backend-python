from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class MessagePagination(PageNumberPagination):
    page_size = 20  # Limit messages per page
    page_size_query_param = 'page_size'  # Allow dynamic page size
    max_page_size = 100  # Set max limit for page size

    def get_paginated_response(self, data):
        return Response({
            'total_messages': self.page.paginator.count,  # Include total count
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })