from rest_framework import serializers
from tagging.models import Tag


class TagSerializer(serializers.ModelSerializer):
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
