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


class Service(models.Model):
    """ Медицинская услуга """
    name = models.CharField(max_length=100, verbose_name='Название мед.услуги')
    description = models.TextField(verbose_name='Описание мед.услуги')
    image = models.ImageField(upload_to='services/', verbose_name='Превью мед.услуги', **NULLABLE)
    price = models.PositiveIntegerField(verbose_name='Цена мед.услуги')
    # Используется Положительное число. Цена не может быть отрицательной.
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    deadline = models.CharField(max_length=100, verbose_name='Срок выполнения мед.услуги')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Мед.услуга"
        verbose_name_plural = "Мед.услуги"
