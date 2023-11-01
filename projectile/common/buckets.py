from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class S3StaticStorage(S3Boto3Storage):
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    custom_domain = settings.STATIC_URL[1:-1]
    default_acl = "public-read"


class S3MediaStorage(S3Boto3Storage):
    bucket_name = settings.AWS_MEDIA_BUCKET_NAME
    custom_domain = settings.MEDIA_URL[1:-1]
    default_acl = "public-read"
    file_overwrite = False
