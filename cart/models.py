from django.db import models
from catalog.models import ShopItem
from accounts.models import CustomUser, Order
# Create your models here.


class Cart(models.Model):
    class Meta:
        verbose_name_plural = 'Корзины'

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(ShopItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return self.item.title