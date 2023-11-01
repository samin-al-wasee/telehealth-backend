from django.conf import settings

import jwt


def encode_jwt_for_user(user):
    return jwt.encode({"slug": str(user.slug)}, settings.SECRET_KEY, algorithm="HS256")


def decode_jwt_for_user(encoded_jwt):
    return jwt.decode(encoded_jwt, settings.SECRET_KEY, algorithms=["HS256"])
