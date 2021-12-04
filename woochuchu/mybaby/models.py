from django.db import models
from accounts.models import User, Animal, Address

# Create your models here.
class MyBaby(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    animal = models.ForeignKey(Animal, on_delete=models.DO_NOTHING)
    body = models.TextField()
    img_url = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'mybaby'

class MyBabyComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mybaby = models.ForeignKey('MyBaby', related_name='comments', on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'mybaby_comment'

class MyBabyLike(models.Model):
    mybaby = models.ForeignKey('MyBaby', related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'mybaby_like'