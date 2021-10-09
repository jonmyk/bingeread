from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Score(models.Model):
	sid		= models.AutoField(primary_key=True)
	uid		= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	bid		= models.CharField(max_length=16)
	score	= models.IntegerField(validators=[
				MinValueValidator(1), MaxValueValidator(10)])

	class Meta:
		constraints = [
			models.UniqueConstraint(fields=['uid', 'bid'],
									name='uid_and_bid_uniq')
		]
