from django.db import models
from django.db.models.fields import BigIntegerField, CharField, DateTimeField, TextField, URLField
from accounts.models import User, Animal, Address
# Create your models here.
class BeMyBaby(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.DO_NOTHING)
    animal = models.ForeignKey(Animal, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=100)
    body = models.TextField()
    img_url = models.URLField()
    phone = models.CharField(max_length=20, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class BeMyBabyComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bemybaby = models.ForeignKey('BeMyBaby', on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


