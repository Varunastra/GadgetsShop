# Generated by Django 2.1.7 on 2019-05-24 21:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('catalog', '0001_initial'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.ShopItem')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Order')),
            ],
            options={
                'verbose_name_plural': 'Корзины',
            },
        ),
    ]