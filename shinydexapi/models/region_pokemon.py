from django.db import models

class RegionPokemon(models.Model):
    pokemon = models.ForeignKey("Pokemon", on_delete=models.CASCADE)
    region = models.ForeignKey("Region", on_delete=models.CASCADE)