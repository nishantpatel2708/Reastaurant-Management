# Generated by Django 3.2.6 on 2021-09-06 12:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rest_admin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PerMonthExpenses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Rent', models.PositiveIntegerField(blank=True, null=True)),
                ('Light_Bill', models.PositiveIntegerField(blank=True, null=True)),
                ('Others', models.PositiveIntegerField(blank=True, null=True)),
                ('res', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Expenses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Day_Expense', models.PositiveIntegerField()),
                ('Date', models.DateTimeField()),
                ('Others', models.PositiveIntegerField(blank=True, null=True)),
                ('res', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
