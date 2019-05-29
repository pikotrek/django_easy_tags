from rest_framework.filters import BaseFilterBackend
from tagging.models import Tag, TaggedItem


class TagLookupFilter(BaseFilterBackend):
    """
    Filter backend used for filtering tags
    """

    def filter_queryset(self, request, queryset, view):
        tag_lookup = request.GET.get('tag')
        if tag_lookup and issubclass(queryset.model, Tag):
            return queryset.filter(name__icontains=tag_lookup)
        return queryset


class GetObjectsByAllTagsFilter(BaseFilterBackend):
    """
    Filter backend used for filtering objects which have assigned all given tags
    """

    def filter_queryset(self, request, queryset, view):
        tags = ','.join(request.GET.getlist('tag'))
        if tags:
            return TaggedItem.objects.get_intersection_by_model(queryset, tags)
        else:
            return queryset


class GetObjectsByAnyTagFilter(BaseFilterBackend):
    """
    Filter backend used for filtering objects which have assigned any of given tag
    """

    def filter_queryset(self, request, queryset, view):
        tags = ','.join(request.GET.getlist('tag'))
        if tags:
            return TaggedItem.objects.get_union_by_model(queryset, tags)
        else:
            return queryset
