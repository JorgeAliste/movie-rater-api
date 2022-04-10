from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Movie(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField(max_length=360)


class Rating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])

    class Meta:
        unique_together = (('user', 'movie'),)
        index_together = (('user', 'movie'),)
