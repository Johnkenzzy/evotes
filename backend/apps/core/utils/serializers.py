"""Defines data serialization helpers."""
from rest_framework import serializers
from django.urls import reverse


def get_general_serializer(model_class):
    """Serializes data generally."""
    class _AutoSerializer(serializers.ModelSerializer):
        links = serializers.SerializerMethodField()

        class Meta:
            model = model_class
            fields = '__all__'
            read_only_fields = ('id', 'created_at', 'updated_at')
            extra_kwargs = {'password': {'write_only': True}}
        
        def get_links(self, obj):
            """Gets the links for the application state"""
            request = self.context.get('request')
            links = {
                "self": request.build_absolute_uri(
                    reverse('organization_detail', args=[obj.id])
                )
            }

            return links
    return _AutoSerializer
