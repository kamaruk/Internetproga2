# Generated by Django 5.1.3 on 2024-11-25 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Краткое описание')),
                ('detailed_description', models.TextField(verbose_name='Подробное описание')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена')),
                ('image', models.ImageField(upload_to='products/', verbose_name='Изображение')),
                ('category', models.CharField(choices=[('Торты', 'Торты'), ('Десерты', 'Десерты'), ('Пирожные', 'Пирожные')], max_length=50, verbose_name='Категория')),
            ],
        ),
    ]