from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
    def update(self, instance, validated_data):
        # Extract password from the validated_data
        password = validated_data.pop('password', None)
        
        # Update the rest of the fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # If password is provided, set the password properly
        if password:
            instance.set_password(password)
        
        # Save the instance
        instance.save()
        return instance