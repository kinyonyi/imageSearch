from django.db import models

# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=100, default="")
    description = models.TextField(default = "")
    cover = models.ImageField(upload_to='images', default="images/default.jpg")

    def __str__(self):
        return str(self.name)
