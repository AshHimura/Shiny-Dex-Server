from django.db import models

class TypePokemon(models.Model):
    pokemon = models.ForeignKey("Pokemon", on_delete=models.CASCADE)
    poketype = models.ForeignKey("PokeType", on_delete=models.CASCADE)