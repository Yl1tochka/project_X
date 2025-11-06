from django.db import models

class Category(models.Model):
    name = models.CharField("Категория", max_length=100, unique=True)
    order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField("Название", max_length=200)
    description = models.TextField("Описание", blank=True)
    price = models.DecimalField("Цена", max_digits=8, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    image = models.ImageField("Фото", upload_to='products/', blank=True, null=True)
    video = models.FileField("Видео (опционально)", upload_to='products/videos/', blank=True, null=True)
    is_available = models.BooleanField("В наличии", default=True)

    class Meta:
        verbose_name = "Блюдо"
        verbose_name_plural = "Блюда"

    def __str__(self):
        return self.name