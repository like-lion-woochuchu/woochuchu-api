from django.db import models
from django.db.models.fields import BigIntegerField, CharField, DateTimeField, TextField, URLField

# Create your models here.
class BeMyBaby(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    img_url = models.URLField()
    phone = models.CharField(max_length=20, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title

class BeMyBabyComment(models.Model):
    bemybaby = models.ForeignKey('BeMyBaby', on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


