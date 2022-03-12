from django.db import models

class ItemPokemon(models.Model):
    pokemon = models.ForeignKey("Pokemon", on_delete=models.CASCADE)
    item = models.ForeignKey("Item", on_delete=models.CASCADE)
    