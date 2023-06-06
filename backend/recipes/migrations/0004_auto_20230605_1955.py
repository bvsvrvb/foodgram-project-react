# Generated by Django 3.2.19 on 2023-06-05 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_alter_cart_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='measurement_unit',
            field=models.CharField(max_length=150, verbose_name='Единицы измерения'),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.CharField(db_index=True, max_length=150, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='name',
            field=models.CharField(db_index=True, max_length=200, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(db_index=True, max_length=150, unique=True, verbose_name='Название'),
        ),
    ]
