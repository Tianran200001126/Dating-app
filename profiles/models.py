from django.contrib.auth.models import User
from django.db import models
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,default=1)
    age = models.PositiveIntegerField()
    bio = models.TextField()
    image = models.ImageField(upload_to='profile_images',blank=True,null=True)

