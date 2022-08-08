import math
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"

    def paginate_queryset(self, queryset, request, view=None):
        page_size = self.get_page_size(request)
        if page_size:
            self.page_size = page_size
        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):

        return Response(self.get_paginated_data(data))

    def get_paginated_data(self, data):

        return {
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "limit": self.page_size,
            "count": self.page.paginator.count,
            "total_pages": math.ceil(self.page.paginator.count / self.page_size),
            "results": data,
        }
