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
        Tag.objects.add_tag(obj, validated_data['name'])
        return obj.tags.get(**validated_data)

    class Meta:
        model = Tag
        fields = ('name',)
