from django.db import models

class Pokemon(models.Model):
    name = models.CharField(max_length=20)
    pokemon_kind = models.CharField(max_length=40)
    description = models.TextField()
    standard_height = models.CharField(max_length=10)
    standard_alpha_height = models.CharField(max_length=10)
    standard_weight = models.FloatField()
    standard_alpha_weight = models.FloatField()
    is_shiny = models.BooleanField(default=False)
    is_alpha = models.BooleanField(default=False)
    home_regions = models.ManyToManyField("Region", through="RegionPokemon")
    poke_types = models.ManyToManyField("PokeType", through="TypePokemon")
    poke_items = models.ManyToManyField("Item", through="ItemPokemon")
    