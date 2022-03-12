from django.db import models

class Favorite(models.Model):
    pokemon = models.ForeignKey("Pokemon", on_delete=models.CASCADE)
    user = models.ForeignKey("DexUser", on_delete=models.CASCADE)
    