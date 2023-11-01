from rest_framework import throttling


class RestrictedRateThrottle(throttling.UserRateThrottle):
    rate = "30/minute"
