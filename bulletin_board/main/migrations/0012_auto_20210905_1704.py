# Generated by Django 3.2.6 on 2021-09-05 14:04

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_ad_is_active'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ArchiveAd',
        ),
        migrations.RemoveField(
            model_name='ad',
            name='tags',
        ),
        migrations.AddField(
            model_name='ad',
            name='tags',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), null=True, size=None, verbose_name='Теги'),
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
    ]
