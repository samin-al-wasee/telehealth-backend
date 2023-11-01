import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from versatileimagefield.serializers import VersatileImageFieldSerializer

from accountio.models import Organization

from common.serializers import BaseModelSerializer

from core.choices import UserType

from patientio.models import Patient

logger = logging.getLogger(__name__)

User = get_user_model()


class BaseUserSerializer(BaseModelSerializer):
    name = serializers.CharField(max_length=100, source="get_name")

    class Meta:
        model = User
        fields = [
            "uid",
            "first_name",
            "last_name",
            "name",
            "date_joined",
            "last_login",
        ]


class MeSerializer(BaseUserSerializer):
    hero = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at1024x256", "crop__1024x256"),
        ],
        required=False,
    )
    avatar = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at256", "crop__256x256"),
            ("at512", "crop__512x512"),
        ],
        required=False,
    )

    class Meta(BaseUserSerializer.Meta):
        fields = [
            "uid",
            "first_name",
            "last_name",
            "email",
            "phone",
            "slug",
            "gender",
            "date_of_birth",
            "status",
        ]
        read_only_fields = [
            "first_name",
            "last_name",
            "phone",
            "status",
        ]


class MePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=50, write_only=True, required=True)
    password = serializers.CharField(
        min_length=8, max_length=50, write_only=True, required=True
    )
    confirm_password = serializers.CharField(
        min_length=8, max_length=50, write_only=True, required=True
    )

    class Meta:
        fields = ("old_password", "password", "confirm_password")

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise ValidationError("Your old password is incorrect.")
        return value

    def validate_password(self, value):
        validate_password(value)
        return value

    def validate(self, data):
        if data.get("password") != data.get("confirm_password"):
            raise ValidationError({"detail": "Passwords must match."})
        return data

    def save(self, *args, **kwargs):
        user = self.context["request"].user
        password = self.validated_data.get("password", None)
        if user and password:
            user.set_password(password)
            user.save(update_fields=["password"])


class UserSerializer(BaseUserSerializer):
    avatar = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at256", "thumbnail__256x256"),
            ("at512", "thumbnail__512x512"),
        ],
        required=False,
    )

    class Meta(BaseUserSerializer.Meta):
        fields = [
            "uid",
            "first_name",
            "last_name",
            "name",
            "date_joined",
            "last_login",
            "avatar",
            "headline",
        ]


class PublicUserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(min_length=2, max_length=50)
    last_name = serializers.CharField(min_length=2, max_length=50)
    password = serializers.CharField(min_length=8, max_length=50, write_only=True)
    organization_uid = serializers.SlugRelatedField(
        queryset=Organization.objects.get_status_editable(),
        slug_field="uid",
        write_only=True,
    )

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "phone",
            "email",
            "weight",
            "height",
            "date_of_birth",
            "gender",
            "social_security_number",
            "blood_group",
            "password",
            "organization_uid",
        )

    def validate_phone(self, value):
        if value and User.objects.filter(phone=value).exists():
            raise ValidationError("This phone number is already taken by another user.")
        return value

    def validate_email(self, value):
        if value and User.objects.filter(email=value).exists():
            raise ValidationError("This email already exists.")
        return value

    def validate_social_security_number(self, value):
        if value and User.objects.filter(social_security_number=value).exists():
            raise ValidationError("This social security number is already exists.")
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        email = validated_data.pop("email", None)
        if email is not None:
            validated_data["email"] = email.lower()
        validated_data["height"] = validated_data.get("height", None)
        validated_data["weight"] = validated_data.get("weight", None)
        validated_data["social_security_number"] = validated_data.get(
            "social_security_number", None
        )

        organization = validated_data.pop("organization_uid")
        user = User.objects.create(
            password=make_password(password),
            type=UserType.PATIENT,
            is_active=True,
            **validated_data,
        )

        Patient.objects.create(user=user, organization=organization)

        return user


class PrivateMeSerializer(BaseModelSerializer):
    class Meta:
        model = User
        fields = [
            "slug",
            "social_security_number",
            "first_name",
            "last_name",
            "phone",
            "email",
            "nid",
            "avatar",
            "status",
            "weight",
            "height",
            "date_of_birth",
            "gender",
            "blood_group",
        ]
        read_only_fields = ["phone", "social_security_number"]

    def validate_email(self, value):
        email = self.context["request"].user.email

        if not email:
            if value and User.objects.filter(email=value).exists():
                raise ValidationError(
                    "This email address is already taken by another user."
                )
        else:
            if value and email == value:
                return value
            if value and User.objects.filter(email=value).exists():
                raise ValidationError(
                    "This email address is already taken by another user."
                )

        return value
