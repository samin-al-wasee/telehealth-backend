from rest_framework import serializers
from versatileimagefield.serializers import VersatileImageFieldSerializer

from mediaroomio.models import MediaImage, MediaImageConnector
from mediaroomio.choices import MediaImageKind


class GlobalImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaImage
        fields = (
            "uid",
            "image",
            "width",
            "height",
            "ppoi",
            "caption",
            "copyright",
            "priority",
        )
        read_only_fields = ("__all__",)


class GlobalImageSlimSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaImage
        fields = (
            "slug",
            "image",
        )
        read_only_fields = ("__all__",)


class GlobalMediaImageConnectorSlimSerializer(serializers.ModelSerializer):
    image = VersatileImageFieldSerializer(
        source="image.image",
        sizes=[
            ("original", "url"),
            ("at256", "crop__256x256"),
            ("at512", "crop__512x512"),
        ],
        read_only=True,
    )

    class Meta:
        model = MediaImageConnector
        fields = ("image",)
        read_only_fields = ("__all__",)


class GlobalMediaImageSerializer(serializers.ModelSerializer):
    uid = serializers.CharField(read_only=True)
    file = serializers.FileField(write_only=True)
    slug = serializers.SlugField(read_only=True)
    width = serializers.IntegerField(write_only=True, allow_null=True, required=False)
    height = serializers.IntegerField(write_only=True, allow_null=True, required=False)
    caption = serializers.CharField(
        write_only=True, allow_null=True, allow_blank=True, required=False
    )
    copyright = serializers.CharField(
        write_only=True, allow_null=True, allow_blank=True, required=False
    )
    kind = serializers.ChoiceField(choices=MediaImageKind.choices)
    image = serializers.ImageField(allow_null=True, read_only=True, required=False)
    fileitem = serializers.FileField(allow_null=True, read_only=True, required=False)

    class Meta:
        model = MediaImage
        fields = [
            "uid",
            "file",
            "slug",
            "width",
            "height",
            "caption",
            "copyright",
            "kind",
            "image",
            "fileitem",
        ]

    def create(self, validated_data):
        file = validated_data.pop("file", None)
        kind = validated_data.get("kind", None)

        if kind == "IMAGE":
            media_image = MediaImage.objects.create(image=file, **validated_data)
        else:
            media_image = MediaImage.objects.create(fileitem=file, **validated_data)

        return media_image
