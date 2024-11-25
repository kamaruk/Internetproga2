from django.db import models


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('Торты', 'Торты'),
        ('Десерты', 'Десерты'),
        ('Пирожные', 'Пирожные'),
    ]

    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Краткое описание")
    detailed_description = models.TextField(verbose_name="Подробное описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    image = models.ImageField(upload_to='products/', verbose_name="Изображение")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, verbose_name="Категория")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ['category', 'name']
