from typing import Dict

from rest_framework_simplejwt.tokens import RefreshToken


def get_user_slug(instance):
    return (
        f"{instance.first_name}-{instance.last_name}-{str(instance.uid).split('-')[0]}"
    )


# Media File Prefixes
def get_user_media_path_prefix(instance, filename):
    return f"users/{instance.slug}/{filename}"


# Generate Token Manually
def get_tokens_for_user(user) -> Dict[str, str]:
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }
