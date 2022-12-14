# Generated by Django 4.1.1 on 2022-11-19 15:31

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('percentage', models.PositiveIntegerField(default=None, help_text='0 to 99%', validators=[django.core.validators.MaxValueValidator(99), django.core.validators.MinValueValidator(0)])),
                ('stripe_coupon_id', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'content"."discount',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200, default=None, null=True, blank=True)),
                ('price', models.DecimalField(decimal_places=0, max_digits=2, validators=[django.core.validators.MinValueValidator(1)])),
                ('src_url', models.URLField(default=None, null=True, blank=True))
            ],
            options={
                'db_table': 'content"."item',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paid', models.BooleanField(default=False)),
                ('discount', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.discount')),
            ],
            options={
                'db_table': 'content"."order',
            },
        ),
        migrations.CreateModel(
            name='Tax',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('percentage', models.PositiveIntegerField(default=20, help_text='0 to 99%', validators=[django.core.validators.MaxValueValidator(99), django.core.validators.MinValueValidator(0)])),
                ('stripe_tax_id', models.CharField(max_length=200)),
                ('inclusive', models.BooleanField(default=False, help_text='True for inclusion tax in price')),
            ],
            options={
                'db_table': 'content"."tax',
            },
        ),
        migrations.CreateModel(
            name='OrderPosition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.item')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.order')),
            ],
            options={
                'db_table': 'content"."order_position',
                'unique_together': {('order', 'item')},
            },
        ),
        migrations.AddField(
            model_name='order',
            name='order_position',
            field=models.ManyToManyField(through='api.OrderPosition', to='api.order'),
        ),
        migrations.AddField(
            model_name='order',
            name='tax',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.tax'),
        ),
    ]
