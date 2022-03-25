from django.db import models

class Post(models.Model):
    publication_date = models.DateField(auto_now_add=True)
    content = models.TextField()
    user = models.ForeignKey("DexUser", on_delete=models.CASCADE)
    