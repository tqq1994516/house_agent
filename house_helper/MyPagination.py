from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class MyPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'size'
    max_page_size = 50

    def get_paginated_response(self, data):
        page_total = self.page.paginator.count // self.page_size + 1
        return Response({
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "total": self.page.paginator.count,
            "page_total": page_total,
            "results": data
        })
