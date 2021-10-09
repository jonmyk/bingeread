from django.db import models
from django.conf import settings
from django.core.validators import MinLengthValidator
from django.db.models.signals import post_delete

class ListMeta(models.Model):
    lid = models.AutoField(primary_key=True)
    uid = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, validators=[MinLengthValidator(1)])
    private = models.BooleanField(default=True) # NOTE: Unimplemented feature
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['uid', 'name'], name='unique_list_name')
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class ListEntry(models.Model):
    lid = models.ForeignKey(ListMeta, on_delete=models.CASCADE)
    bid =  models.CharField(max_length=20, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['lid', 'bid'], name='unique_book_entry')
        ]

    def __str__(self):
        return self.bid

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class BookMeta(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    selfLink = models.URLField()
    volumeInfo = models.JSONField()

    def __str__(self):
        return self.id


def delete_book(sender, instance, **kwargs):
    """
    Deleting locally stored data if there is no references to the book in any list.
    This method is called each time a ListEntry record is deleted.
    """
    if ListEntry.objects.filter(bid=instance).count() == 0:
        BookMeta.objects.filter(id=instance).delete() 


post_delete.connect(delete_book, sender=ListEntry)

