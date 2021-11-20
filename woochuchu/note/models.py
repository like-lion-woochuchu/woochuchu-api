from django.db import models
from accounts.models import User

# # Create your models here.
# class Note(models.Model):
#     sender = models.ForeignKey(User, on_delete=models.CASCADE)
#     receiver = models.ForeignKey(User, on_delete=models.CASCADE)
#     body = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         managed = False
#         db_table = 'note'