from django.db import models

# little tweak for Meta attributes
models.options.DEFAULT_NAMES += ('qb',)

# Create your models here.
class Feature(models.Model):
    """ Model class that holds all query instances """
    name = models.CharField(max_length=255, default="")
    slug = models.SlugField(max_length=50, default="")
    model_verbose_name = models.CharField(max_length=255, choices=(), default="")
    limit = models.IntegerField(default=0)
    order_by = models.CharField(max_length=255, choices=(), default="")
    order_asc = models.BooleanField(default=False)
    template = models.CharField(max_length=255, default="")

    def __str__(self):
        return self.name

    class Meta:
        qb = True

class Query(models.Model):
    """ Model for a single query """
    field_verbose_name = models.CharField(max_length=255, default="")    
    FILTERS = (
        ('Equals', 'Equals'),
        ('Greater than', 'Greater than'),
        ('Less than', 'Less than'),
        # ('Range', 'Range'),
        ('Contains', 'Contains'),
    )
    filter_criteria = models.CharField(max_length=255, default="", choices=FILTERS)
    filter_value = models.CharField(max_length=255, default=None, blank=True)
    JOIN_F = (
        ('-', '-'),
        ('AND', 'AND'),
        ('OR', 'OR'),
    )
    join = models.CharField(max_length=255, default="-", choices=JOIN_F)
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.field_verbose_name
    
    class Meta:
        verbose_name_plural = 'Queries'
        qb = True

class Contact(models.Model):
    name = models.CharField(max_length=255)
    number = models.CharField(max_length=50)

    def __str__(self):
        return self.name
