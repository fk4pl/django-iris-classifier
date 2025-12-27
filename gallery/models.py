from django.db import models


class IrisSample(models.Model):
    instance_id = models.PositiveIntegerField(unique=True)
    sepal_length = models.FloatField()
    sepal_width = models.FloatField()
    petal_length = models.FloatField()
    petal_width = models.FloatField()
    SPECIES_CHOICES = [
        ('setosa', 'Iris setosa'),
        ('versicolor', 'Iris versicolor'),
        ('virginica', 'Iris virginica'),
    ]
    species = models.CharField(max_length=32, choices=SPECIES_CHOICES)

    def __str__(self):
        return f"{self.instance_id} - {self.species}"


class Collection(models.Model):
    # A simple model not related to auth, with many-to-many to IrisSample
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    owner_name = models.CharField(max_length=100)
    public = models.BooleanField(default=False)
    samples = models.ManyToManyField(IrisSample, blank=True, related_name='collections')

    def __str__(self):
        return self.title
