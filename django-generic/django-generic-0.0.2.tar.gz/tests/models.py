from django.db import models


class ExampleModel(models.Model):
    """
    Example test model, created for testing some db functions.
    """
    name = models.CharField(max_length=64)
    field1 = models.CharField(max_length=64)
