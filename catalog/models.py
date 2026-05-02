from django.conf import settings
from django.db import models


class Category(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Наименование',
        help_text='Введите наименование категории',
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание',
        help_text='Введите описание категории',
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Наименование',
        help_text='Введите наименование продукта',
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание',
        help_text='Введите описание продукта',
    )
    image = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True,
        verbose_name='Изображение',
        help_text='Загрузите изображение продукта',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Категория',
        help_text='Выберите категорию',
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена за покупку',
        help_text='Введите цену за покупку',
    )
    is_published = models.BooleanField(
        default=False,
        verbose_name='Опубликован',
        help_text='Отметка публикации продукта',
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='products',
        verbose_name='Владелец',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата последнего изменения',
    )

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['-created_at']
        permissions = [
            ('can_unpublish_product', 'Can unpublish product'),
        ]

    def __str__(self):
        return self.name