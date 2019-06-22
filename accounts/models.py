from django.contrib.auth.models import AbstractUser
from django.db import models
from catalog.models import ShopItem

# Create your models here
# .
# class Gender(models.Model):
#     choices = (("Male", "Мужской"), ("Female", "Женский"))
#     name = models.CharField(max_length=50, choices=choices)


class CustomUser(AbstractUser):
    choices = (("Male", "Мужской"), ("Female", "Женский"))
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    town = models.CharField(max_length=50)
    age = models.IntegerField(default=30)
    gender = models.CharField(max_length=50, choices=choices, default=choices[0][0])


class ProfitUser(models.Model):
    class Meta:
        verbose_name_plural = "Выгодные пользователи"

    price = models.IntegerField()
    category = models.CharField(max_length=50)
    user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)

    def __str__(self):
        return "Пользователь " + self.user.username


class Order(models.Model):
    class Meta:
        verbose_name_plural = "Заказы"

    date = models.DateField()
    status = models.CharField(max_length=200)
    user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)

    def __str__(self):
        return "Заказ пользователя " + self.user.username


class Feedback(models.Model):
    item = models.ForeignKey(ShopItem, on_delete=models.PROTECT)
    date = models.DateField()
    message = models.CharField(max_length=300)
    rating = models.IntegerField()
    user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)


class Discount(models.Model):
    class Meta:
        verbose_name_plural = "Скидки"

    def __str__(self):
        return self.info

    info = models.CharField(max_length=200)
    code = models.CharField(max_length=100)
    choices = (
        ("0.5", "50%"),
        ("0.4", "40%"),
        ("0.3", "30%"),
        ("0.2", "20%"),
        ("0.1", "10%"),
    )
    amount = models.CharField(choices=choices, default=choices[0][0], max_length=10)
