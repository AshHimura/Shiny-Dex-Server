from django.db import models

class Pokemon(models.Model):
    name = models.CharField(max_length=20)
    pokemonKind = models.CharField(max_length=40)
    description = models.TextField()
    height = models.FloatField()
    weight = models.FloatField()
    items = models.ForeignKey("Item", on_delete=models.CASCADE)
    isShiny = models.BooleanField(default=False)
    isAlpha = models.BooleanField(default=False)
    