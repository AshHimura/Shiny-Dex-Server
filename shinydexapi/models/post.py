from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=300)
    publication_date = models.DateField(auto_now_add=True)
    image_url = models.ImageField(null=True)
    content = models.TextField()
    user = models.ForeignKey("DexUser", on_delete=models.CASCADE)
    