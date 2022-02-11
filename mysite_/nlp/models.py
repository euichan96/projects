from django.db import models

# Create your models here.


class Review(models.Model):
    review = models.TextField()
    answer = models.PositiveSmallIntegerField(default=0)
    create_date = models.DateTimeField()

    def __str__(self):
        return self.review