# Generated by Django 3.2.6 on 2021-08-31 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_rest',
            field=models.BooleanField(default=False),
        ),
    ]
