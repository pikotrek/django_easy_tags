from django.conf import settings
from rest_framework import serializers
from tagging.models import Tag

ERROR_DICT_PROVIDED = 'error_dict_provided'


class TagSerializer(serializers.ModelSerializer):
    default_error_messages = {
        ERROR_DICT_PROVIDED: 'Tags should be a list of tag names.'
    }

    def validate(self, attrs):
        data = attrs.get('name')
        try:
            assert not isinstance(data, dict), ERROR_DICT_PROVIDED
        except AssertionError as e:
            self.fail(str(e))
        return attrs

    def to_internal_value(self, data):
        return {'name': data}

    def to_representation(self, instance):
        return instance.name

    def create(self, validated_data):
        obj = self.context['obj']
        tag_name = validated_data['name']
        if getattr(settings, 'FORCE_LOWERCASE_TAGS', False):
            tag_name = tag_name.lower()
        Tag.objects.add_tag(obj, tag_name)
        return Tag.objects.get(name=tag_name)

    class Meta:
        model = Tag
        fields = ('name',)
