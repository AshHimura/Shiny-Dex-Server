from django.db import models

class PokeType(models.Model):
    poketype = models.CharField(max_length=10)