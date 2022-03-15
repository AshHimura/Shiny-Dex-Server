from django.db import models

class TypePokemon(models.Model):
    pokemon = models.ForeignKey("Pokemon", on_delete=models.CASCADE)
    type = models.ForeignKey("Type", on_delete=models.CASCADE)