from rest_framework.filters import BaseFilterBackend


class TolkienBooksFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(author__last_name='Tolkien')
