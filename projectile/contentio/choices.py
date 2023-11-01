from django.db import models


class RatingChoices(models.IntegerChoices):
    ZERO_STAR = 0, "0"
    ONE_STAR = 1, "1"
    TWO_STARS = 2, "2"
    THREE_STARS = 3, "3"
    FOUR_STARS = 4, "4"
    FIVE_STARS = 5, "5"
