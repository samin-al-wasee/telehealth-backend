from django.db.models import Q

from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from core.models import User
from core.utils import get_tokens_for_user


class PublicUserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=255,
        help_text="You can login by phone number, email or social security number",
        write_only=True,
    )
    password = serializers.CharField(min_length=6, max_length=50, write_only=True)
    refresh = serializers.CharField(read_only=True)
    access = serializers.CharField(read_only=True)

    def create(self, validated_data):
        username = validated_data.get("username")
        password = validated_data.get("password")
        try:
            user: User = User.objects.get(
                Q(email=username)
                | Q(phone=username)
                | Q(social_security_number=username)
            )
            if not user.check_password(password):
                raise AuthenticationFailed()

            token = get_tokens_for_user(user)
            validated_data["refresh"] = token["refresh"]
            validated_data["access"] = token["access"]

            return validated_data

        except User.DoesNotExist:
            raise AuthenticationFailed()
