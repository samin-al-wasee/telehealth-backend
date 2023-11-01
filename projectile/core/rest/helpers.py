from rest_framework.generics import get_object_or_404

from ..models import User
from ..choices import UserStatus


def get_user_or_404(slug):
    return get_object_or_404(User, slug=slug, is_active=True, status=UserStatus.ACTIVE)
