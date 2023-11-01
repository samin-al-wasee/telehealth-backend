from rest_framework.pagination import PageNumberPagination


class LargeResultsSetPagination(PageNumberPagination):
    max_page_size = 200
    page_size = 200
    page_size_query_param = "page_size"
