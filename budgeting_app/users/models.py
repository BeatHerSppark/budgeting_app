from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total = models.FloatField(default=0)
    budget = models.FloatField(default=0)

    def __str__(self):
        return self.user.username
