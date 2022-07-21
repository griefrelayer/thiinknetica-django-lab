# Generated by Django 3.2.6 on 2021-08-22 00:33

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import main.utils
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customuser', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название объявления')),
                ('description', models.CharField(max_length=500, verbose_name='Описание')),
                ('datetime_created', models.DateTimeField(auto_now_add=True, verbose_name='Дата/время создания')),
                ('datetime_modified', models.DateTimeField(auto_now=True, verbose_name='Дата/время изменения')),
                ('price', models.PositiveIntegerField(default=1, verbose_name='Цена')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='customuser.user')),
                ('inn', models.CharField(default='000000000000', max_length=12, validators=[main.utils.validate_inn], verbose_name='ИНН')),
                ('picture', sorl.thumbnail.fields.ImageField(default='uploads/seller_pics/default.jpg', upload_to='uploads/seller_pics/')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('customuser.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('ad_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.ad')),
                ('brand', models.CharField(max_length=50, verbose_name='Марка')),
                ('mileage', models.PositiveIntegerField(verbose_name='Пробег')),
                ('color', models.CharField(max_length=50, verbose_name='Цвет')),
            ],
            options={
                'abstract': False,
            },
            bases=('main.ad',),
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('ad_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.ad')),
                ('area', models.CharField(max_length=100, verbose_name='Доступно в')),
            ],
            options={
                'abstract': False,
            },
            bases=('main.ad',),
        ),
        migrations.CreateModel(
            name='Thing',
            fields=[
                ('ad_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.ad')),
                ('weight', models.PositiveIntegerField(verbose_name='Вес')),
                ('size', models.CharField(blank=True, max_length=50, verbose_name='Размеры')),
            ],
            options={
                'abstract': False,
            },
            bases=('main.ad',),
        ),
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subscribed_to', models.CharField(max_length=30, verbose_name='На что подписан')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Подписчик(пользователь)')),
            ],
        ),
        migrations.AddField(
            model_name='ad',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.category', verbose_name='Категория'),
        ),
        migrations.AddField(
            model_name='ad',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.seller', verbose_name='Продавец'),
        ),
        migrations.AddField(
            model_name='ad',
            name='tags',
            field=models.ManyToManyField(to='main.Tag', verbose_name='Теги'),
        ),
        migrations.CreateModel(
            name='ArchiveAd',
            fields=[
            ],
            options={
                'ordering': ['datetime_created'],
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('main.ad',),
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pic', sorl.thumbnail.fields.ImageField(upload_to='uploads/car_pics/')),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.car')),
            ],
        ),
    ]