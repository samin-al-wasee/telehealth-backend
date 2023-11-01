import random


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[-1].strip()
    elif request.META.get("HTTP_X_REAL_IP"):
        ip = request.META.get("HTTP_X_REAL_IP")
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def unique_number_generator(instance) -> int:
    model = instance.__class__
    unique_number = random.randint(111111, 9999999)
    if model.objects.filter(serial_number=unique_number).exists():
        unique_number_generator(instance)
    return unique_number
