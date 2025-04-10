"""Defines data serialization helpers."""
from rest_framework import serializers


def get_general_serializer(model_class):
    """Serializes data generally."""
    class _AutoSerializer(serializers.ModelSerializer):
        class Meta:
            model = model_class
            fields = '__all__'
            read_only_fields = ('id', 'created_at', 'updated_at')
    return _AutoSerializer
