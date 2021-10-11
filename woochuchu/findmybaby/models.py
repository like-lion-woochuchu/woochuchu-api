from django.db import models
from accounts.models import User, Animal, Address
# Create your models here.

class FindMyBaby(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.DO_NOTHING)
    animal = models.ForeignKey(Animal, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=20)
    breed = models.CharField(max_length=45)
    sex = models.IntegerField()
    age = models.IntegerField()
    last_seen = models.DateTimeField()
    title = models.CharField(max_length=45)
    body = models.TextField()
    img_url = models.URLField()
    phone = models.CharField(max_length=20, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'findmybaby'


class FindMyBabyComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    findmybaby = models.ForeignKey("FindMyBaby", related_name="comments", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        managed = False
        db_table = 'findmybaby_comment'