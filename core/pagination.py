from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    """Supports ?page_size=N (max 100). Default page size set in settings.PAGE_SIZE."""
    page_size_query_param = 'page_size'
    max_page_size         = 100
