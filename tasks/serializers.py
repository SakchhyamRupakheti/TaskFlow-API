from rest_framework import serializers
from .models import Task
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "owner",
            "title",
            "description",
            "status",
            "created_at",
        ]
        read_only_fields = ["id", "created_at", "owner"]

    def validate_title(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Title cannot be empty or contain only spaces."
            )

        if len(value) < 3:
            raise serializers.ValidationError(
                "Title must contain at least 3 characters."
            )

        return value
    
User = get_user_model()
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only = True,
        validators = [validate_password],
    )
    
    class Meta:
        model = User
        fields = ["username", "password"]
        
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
