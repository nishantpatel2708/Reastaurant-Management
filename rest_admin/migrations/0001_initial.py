# Generated by Django 3.2.6 on 2021-08-31 12:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Category_Name', models.CharField(max_length=50)),
                ('Category_Image', models.ImageField(upload_to='category_images')),
                ('Description', models.CharField(max_length=100)),
                ('rest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table_no', models.CharField(max_length=120)),
                ('status', models.CharField(max_length=20)),
                ('qr', models.ImageField(null=True, upload_to='qr_code')),
                ('rest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MenuTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Dish_image', models.ImageField(blank=True, null=True, upload_to='dish_images/')),
                ('Dish_Name', models.CharField(max_length=50)),
                ('Dish_Description', models.CharField(max_length=80)),
                ('Price', models.PositiveIntegerField()),
                ('pices', models.CharField(blank=True, max_length=30, null=True)),
                ('status', models.CharField(max_length=20)),
                ('speciality', models.BooleanField(default=False)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rest_admin.categories')),
                ('res', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
