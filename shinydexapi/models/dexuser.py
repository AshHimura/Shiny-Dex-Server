from django.db import models
from django.contrib.auth.models import User

class DexUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    