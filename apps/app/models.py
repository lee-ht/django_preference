from django.db import models


class RawData(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    name = models.CharField(max_length=50, unique=True)
    value = models.IntegerField(null=False)
