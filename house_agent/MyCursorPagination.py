from rest_framework.pagination import CursorPagination


class MyCursorPagination(CursorPagination):
    page_size = 10
    page_size_query_param = 'size'
    max_page_size = 50
    ordering = '-pk'