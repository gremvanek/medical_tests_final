from django.conf import settings
from django.db import models

NULLABLE = {'null': True, 'blank': True}


class Category(models.Model):
    """ Категории услуг """
    name = models.CharField(max_length=100, verbose_name='Название категории')
    description = models.TextField(verbose_name='Описание услуги')
    image = models.ImageField(upload_to='categories/', verbose_name='Изображение', **NULLABLE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
