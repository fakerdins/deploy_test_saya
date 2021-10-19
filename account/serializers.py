from django.db.models import fields
from rest_framework import serializers
from .utils import send_activation_code
from .models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        min_length=4,required=True,
        write_only=True
    )
    password_confirmation = serializers.CharField(
        min_length=4,required=True,
        write_only=True
    )

    class Meta:
        model = CustomUser
        fields = (
            'email', 'password',
            'password_confirmation'
        )
    
    def validate(self, attrs):
        password = attrs.get('password')
        password_confirmation = attrs.pop('password_confirmation')
        if password != password_confirmation:
            msg_ = ("Passwords are not matching...")
            raise serializers.ValidationError(msg_)
        return attrs

    def create(sefl, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        send_activation_code(
            user.email,
            user.activation_code
        )
        return user

    
