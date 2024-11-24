from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.ImageField(upload_to="category_icons/")

    def __str__(self):
        return self.name

class PopularService(models.Model):
    title = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    reviews_count = models.IntegerField()
    image = models.ImageField(upload_to="service_images/")

    def __str__(self):
        return self.title

