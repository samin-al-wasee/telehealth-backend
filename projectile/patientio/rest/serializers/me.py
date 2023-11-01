from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from versatileimagefield.serializers import VersatileImageFieldSerializer

from appointmentio.models import SeekHelp

from ...models import Patient

User = get_user_model()


class PrivatePatientDetailSerializer(serializers.ModelSerializer):
    avatar = VersatileImageFieldSerializer(
        source="user.avatar",
        sizes=[
            ("original", "url"),
            ("at256", "crop__256x256"),
            ("at512", "crop__512x512"),
        ],
        required=False,
    )
    first_name = serializers.CharField(source="user.first_name", required=False)
    last_name = serializers.CharField(source="user.last_name", required=False)
    email = serializers.CharField(source="user.email", required=False)
    language = serializers.CharField(source="user.language", required=False)
    phone = serializers.CharField(source="user.phone", read_only=True)
    social_security_number = serializers.CharField(
        source="user.social_security_number", read_only=True
    )
    nid = serializers.CharField(source="user.nid", required=False)
    hero = serializers.ImageField(source="user.hero", required=False)
    gender = serializers.CharField(source="user.gender", required=False)
    date_of_birth = serializers.DateField(source="user.date_of_birth", required=False)
    height = serializers.CharField(source="user.height", required=False)
    weight = serializers.CharField(source="user.weight", required=False)
    blood_group = serializers.CharField(source="user.blood_group", required=False)

    class Meta:
        model = Patient
        fields = [
            "uid",
            "first_name",
            "last_name",
            "email",
            "language",
            "phone",
            "social_security_number",
            "nid",
            "hero",
            "gender",
            "date_of_birth",
            "height",
            "weight",
            "blood_group",
            "avatar",
        ]

    def validate_email(self, value):
        if value and User.objects.filter(email=value).exists():
            raise ValidationError("This email already exists.")
        return value

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", {})

        user = instance.user
        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()

        return super().update(instance, validated_data)


class PrivatePatientSeekHelpSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeekHelp
        fields = ["uid", "name"]
        read_only_fields = ("__all__",)
