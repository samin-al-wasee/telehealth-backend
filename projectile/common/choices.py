from django.db import models


class Currency(models.TextChoices):
    USD = "USD", "USD"
    EUR = "EUR", "EUR"
    DKK = "DKK", "DKK"
    SEK = "SEK", "SEK"
    NOK = "NOK", "NOK"
