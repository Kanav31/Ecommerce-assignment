from rest_framework.pagination import LimitOffsetPagination


class CustomPageNumberPagination(LimitOffsetPagination):
    """
    Limit/offset pagination — standard for production APIs.
    Query params: ?limit=N&offset=N  (default limit from settings.PAGE_SIZE, max 100)
    Response shape: { count, next, previous, results }
    """
    max_limit = 100
