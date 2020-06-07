from django.db import models
from django.urls import reverse

# Create your models here.


class ProductCategory(models.Model):
    name = models.CharField(verbose_name="имя", max_length=64, unique=True)
    slug = models.SlugField(max_length=255, verbose_name='Url', unique=True)
    is_active = models.BooleanField(verbose_name="категория активна", default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Tag(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, verbose_name='Url', unique=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class Products(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    title = models.CharField(verbose_name="имя продукта", max_length=50)
    slug = models.SlugField(max_length=255, verbose_name='Url', unique=True)
    content = models.TextField(verbose_name="описание продукта", blank=True)
    created_at = models.DateTimeField(verbose_name="дата добавления в каталог", auto_now_add=True)
    photo = models.ImageField(upload_to="products_images", blank=True)
    price = models.DecimalField(verbose_name="цена продукта", max_digits=8, decimal_places=2, default=0)
    quantity = models.DecimalField(verbose_name="Продуктов в наличии", max_digits=5, decimal_places=0, default=0)
    is_active = models.BooleanField(verbose_name="категория активна", default=True)

    def get_absolute_url(self):
        return reverse('products', kwargs={"slug": self.slug})

    def __str__(self):
        return f"{self.title} ({self.category.name})"

    class Meta:
        ordering = ['-created_at']



