from django.db import models

class Pokemon(models.Model):
    name = models.CharField(max_length=20)
    pokemonKind = models.CharField(max_length=40)
    description = models.TextField()
    standardHeight = models.CharField(max_length=10)
    standardAlphaHeight = models.CharField(max_length=10)
    standardWeight = models.FloatField()
    standardAlphaWeight = models.FloatField()
    isShiny = models.BooleanField(default=False)
    isAlpha = models.BooleanField(default=False)
    home_regions = models.ManyToManyField("Region", through="regionpokemon")
    poke_types = models.ManyToManyField("Type", through="typepokemon")
    poke_items = models.ManyToManyField("Item", through="")