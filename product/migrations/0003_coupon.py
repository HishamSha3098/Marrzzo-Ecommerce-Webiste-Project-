# Generated by Django 4.1.5 on 2023-02-20 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_ad_to_cart_created_at_ad_to_cart_quantity'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50)),
                ('discount', models.FloatField()),
                ('valid_from', models.DateTimeField()),
                ('valid_to', models.DateTimeField()),
                ('active', models.BooleanField()),
            ],
        ),
    ]
