from django.db import models

# Create your models here.
from django.db import models

class ApiData(models.Model):
    url = models.URLField(unique=True)
    data = models.JSONField()

    def __str__(self):
        return self.url
