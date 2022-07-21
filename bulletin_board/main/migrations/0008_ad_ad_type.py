# Generated by Django 3.2.6 on 2021-09-02 20:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('main', '0007_remove_ad_ad_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='ad_type',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
    ]
