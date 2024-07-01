from django.db import models
from django.urls import reverse


class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=255, blank=True)
    Category_image = models.ImageField(upload_to='photos/categoris', blank=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def category_url(self):
        return reverse('category', args=[self.slug])

    def __str__(self):
        return self.category_name
