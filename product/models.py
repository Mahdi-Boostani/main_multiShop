from django.db import models


class Size(models.Model):
    title = models.CharField(max_length=150)

    class Meta:
        verbose_name = 'سایز'
        verbose_name_plural = 'سایزها'

    def __str__(self):
        return self.title


class Color(models.Model):
    title = models.CharField(max_length=150)

    class Meta:
        verbose_name = 'رنگ'
        verbose_name_plural = 'رنگ ها'

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=150)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='products')
    size = models.ManyToManyField(Size, related_name='product_size', blank=True)
    color = models.ManyToManyField(Color, related_name='product_image', blank=True)
    count = models.SmallIntegerField()

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'

    def __str__(self):
        return self.title



