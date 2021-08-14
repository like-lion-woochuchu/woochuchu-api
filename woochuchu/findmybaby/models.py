from django.db import models

# Create your models here.
class FindMyBaby(models.Model):
    # USER 추가
    # LOCATION 추가
    # ANIMAL 추가
    title = models.CharField(max_length=20)
    body = models.TextField()
    img_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    phone = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.title

class FindMyBabyComment(models.Model):
    # USER 추가
    body = models.TextField()
    findmybaby = models.ForeignKey("FindMyBaby", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.body