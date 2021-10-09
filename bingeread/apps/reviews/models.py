from django.db import models
from django.conf import settings

from django.utils import timezone

class Reviews(models.Model):
    sid = models.AutoField(primary_key=True)
    uid = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bid = models.CharField(max_length=16)
    comment = models.CharField(max_length=200)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.comment
