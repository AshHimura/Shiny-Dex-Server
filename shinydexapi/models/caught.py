from django.db import models

class Caught(models.Model):
    user = models.ForeignKey("DexUser", on_delete=models.CASCADE)
    pokemon = models.ForeignKey("Pokemon", on_delete=models.CASCADE)
    is_shiny = models.BooleanField(default=True)
    is_alpha = models.BooleanField(default=False)
    