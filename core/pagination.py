from rest_framework.pagination import LimitOffsetPagination

class CustomPageNumberPagination(LimitOffsetPagination):
    max_limit = 100
