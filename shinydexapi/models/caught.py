from django.db import models

class Caught(models.Model):
    user = models.ForeignKey("DexUser", on_delete=models.CASCADE)
    pokemon = models.ForeignKey("Pokemon", on_delete=models.CASCADE)
    isShiny = models.BooleanField(default=True)
    isAlpha = models.BooleanField(default=False)
    