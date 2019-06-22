from django.db import models
from django.utils.text import slugify

# Create your models here.


def imagePath(instance, filename):
    return "{0}/{1}".format(instance.slug, filename)


def setCategory(category, slug):
    item = ShopItem.objects.get(slug=slug)
    item.category = category
    item.save()


class ShopItem(models.Model):
    class Meta:
        pass

    price = models.DecimalField(max_digits=9, decimal_places=2, default="0", verbose_name='Цена')
    first_image = models.ImageField(null='media/no_image.png', upload_to=imagePath, verbose_name='Первое фото')
    second_image = models.ImageField(null='media/no_image.png', upload_to=imagePath, verbose_name='Второе фото')
    title = models.CharField(max_length=120, default="", verbose_name='Заголовок')
    manufacter = models.CharField(max_length=50, default="",  verbose_name='Изготовитель')
    slug = models.SlugField(unique=True, blank=True, editable=False)
    RATING_CHOICHES = [(i, str(i)) for i in range(1, 6)]
    rating = models.IntegerField(choices=RATING_CHOICHES, default=1, verbose_name='Рейтинг')
    category = models.CharField(max_length=20, editable=False)
    clicks = models.IntegerField(editable=False, default=0)

    def __str__(self):
        return self.title

    def _get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while ShopItem.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)


class Device(ShopItem):
    class Meta:
        pass

    os = models.CharField(max_length=50, default="Android", verbose_name='Система')
    year = models.IntegerField(default=2010, verbose_name='Год')
    camera = models.IntegerField(default=8, verbose_name='Камера')
    display = models.CharField(max_length=50, default="1920x1080", verbose_name='Разрешение')
    battery = models.IntegerField(default=1000, verbose_name='Батарея')
    capacity = models.IntegerField(default=1800, verbose_name='Вместимость')
    chip = models.CharField(max_length=50, default="MTK", verbose_name='Процессор')
    color = models.CharField(max_length=50, default="черный", verbose_name='Цвет')
    has_wifi = models.BooleanField(default=True, verbose_name='Есть Wi-fi?')
    weight = models.IntegerField(default=400, verbose_name='Вес')


class Tablet(Device):
    class Meta:
        verbose_name_plural = 'Планшеты'

    has_pen = models.BooleanField(verbose_name='Есть стилус?')
    has_keyboard = models.BooleanField(verbose_name='Есть клавиатура?')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        setCategory('tablets', self.slug)


class Phone(Device):
    class Meta:
        verbose_name_plural = 'Телефоны'

    access = models.CharField(max_length=50, verbose_name='Доступ')
    sim_format = models.CharField(max_length=50, verbose_name='Поддерживаемый формат SIM')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        setCategory('phones', self.slug)


class Accessorie(ShopItem):
    class Meta:
        pass

    type = models.CharField(max_length=50, verbose_name='Тип')
    color = models.CharField(max_length=50, verbose_name='Цвет')


class Cable(Accessorie):
    class Meta:
        verbose_name_plural = 'Кабеля'

    features = models.CharField(max_length=50, verbose_name='Вход')
    compatibility = models.CharField(max_length=50, verbose_name='Выход')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        setCategory('cables', self.slug)


class Sdcard(Accessorie):
    class Meta:
        verbose_name_plural = 'SD-карты'

    capacity = models.IntegerField(verbose_name='Вместимость')
    speed = models.IntegerField(verbose_name='Скорость записи')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        setCategory('sdcards', self.slug)


class Headphone(Accessorie):
    class Meta:
        verbose_name_plural = 'Наушники'

    communication = models.CharField(max_length=50, verbose_name='Соединение')
    frequency = models.CharField(max_length=50, verbose_name='Максимальная частота')
    connectors = models.CharField(max_length=50, verbose_name='Разьем')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        setCategory('headphones', self.slug)


class Cover(Accessorie):
    class Meta:
        verbose_name_plural = 'Чехлы'

    material = models.CharField(max_length=50, verbose_name='Материал')
    design = models.CharField(max_length=50, verbose_name='Дизайн')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        setCategory('covers', self.slug)