from django.db import models
from accounts.models import User, Animal, Address


class BeMyBaby(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.DO_NOTHING)
    address_detail = models.CharField(max_length=100, blank=True)
    animal = models.ForeignKey(Animal, on_delete=models.DO_NOTHING)
    breed = models.CharField(max_length=45)
    sex = models.IntegerField()
    age = models.IntegerField(null=True)
    description = models.CharField(max_length=200)
    img_url = models.TextField()
    phone = models.CharField(max_length=20, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    adopt_flag = models.IntegerField()
    
    class Meta:
        managed = False
        db_table = 'bemybaby'


class BeMyBabyComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bemybaby = models.ForeignKey('BeMyBaby', related_name="comments", on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'bemybaby_comment'
