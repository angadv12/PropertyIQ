from rest_framework import serializers
from .models import HouseListing

class HouseListingSerializer(serializers.ModelSerializer):
    choice_fields = serializers.SerializerMethodField()

    class Meta:
        model = HouseListing
        fields = "__all__"
        extra_kwargs = {
            "author": {"read_only": True},
            "predicted_price": {"read_only": True},
        }
    
    def get_choice_fields(self, obj):
        choice_fields = {}
        for field in obj._meta.fields:
            if hasattr(field, 'choices') and field.choices:
                value = getattr(obj, field.name)
                choice_fields[field.name] = {
                    'key': value,
                    'display': dict(field.choices).get(value, value)
                }
        return choice_fields

    def create(self, validated_data):
        return HouseListing.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'HouseImage':
                if value is not None:
                    instance.HouseImage = value
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance