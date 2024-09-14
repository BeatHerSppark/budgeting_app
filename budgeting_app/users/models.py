from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total = models.FloatField(default=0)
    budget = models.FloatField(default=0)
    currency = models.CharField(max_length=10, default='USD')
    pfpUrl = models.CharField(max_length=255, default="https://static.vecteezy.com/system/resources/previews/009/292/244/non_2x/default-avatar-icon-of-social-media-user-vector.jpg")

    def __str__(self):
        return self.user.username
