# Generated by Django 4.2.2 on 2023-06-20 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('www', '0004_delete_userfollows'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='body',
            field=models.TextField(blank=True, max_length=8192),
        ),
    ]
