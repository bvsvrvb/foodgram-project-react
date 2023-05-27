from rest_framework import pagination

DEFAULT_PAGE_SIZE = 10


class CustomPageNumberPagination(pagination.PageNumberPagination):
    page_size_query_param = 'limit'
    page_size = DEFAULT_PAGE_SIZE
