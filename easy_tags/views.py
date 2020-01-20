from django.core.exceptions import ObjectDoesNotExist
from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from tagging.models import Tag

from easy_tags.filters import TagLookupFilter
from easy_tags.serializers import TagSerializer


class ConfigurableViewMixin(object):
    config = None

    def __init__(self, config=None):
        self.config = config


class ConfigurableViewSet(
    GenericViewSet,
    ConfigurableViewMixin
):
    pagination_class = None

    def __init__(self, config=None):
        super(ConfigurableViewSet, self).__init__(config=config)

    def get_permissions(self):
        if self.config['permissions']:
            self.permission_classes = self.config['permissions']
        return super(ConfigurableViewSet, self).get_permissions()


class TaggingView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    ConfigurableViewSet
):
    pagination_class = None
    serializer_class = TagSerializer
    filter_backends = [TagLookupFilter]

    def __init__(self, config=None):
        super(TaggingView, self).__init__(config=config)

    def get_queryset(self):
        obj = self._lazy_object
        if obj:
            return obj.tags.all().order_by('name')
        else:
            return Tag.objects.none()

    def get_serializer_context(self):
        context = super(TaggingView, self).get_serializer_context()
        context['obj'] = self._lazy_object
        return context

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        del self._lazy_object.tags
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @property
    def _lazy_object(self):
        if not hasattr(self, '_lazy_obj'):
            try:
                obj = self.config['content_type'].get_object_for_this_type(pk=self.kwargs.get(self.lookup_field))
            except ObjectDoesNotExist:
                obj = None
            setattr(self, '_lazy_obj', obj)
        return getattr(self, '_lazy_obj')


class AllTagsView(
    mixins.ListModelMixin,
    ConfigurableViewSet
):
    serializer_class = TagSerializer
    filter_backends = [TagLookupFilter]

    def get_queryset(self):
        model_class = self.config['content_type'].model_class()
        queryset = getattr(model_class, '_default_manager').all()
        for backend in list(self.config.get('filters', [])):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return model_class.tags.filter(items__object_id__in=queryset).order_by('name')
