# Generated by Django 5.1.6 on 2025-07-18 14:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=15)),
                ('price', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='StoreImages/')),
                ('A_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('B_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('C_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('discount_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('description', models.CharField(blank=True, max_length=300, null=True)),
                ('label', models.CharField(blank=True, choices=[('NEW', 'NEW'), ('FEATURED', 'FEATURED'), ('SPECIAL', 'SPECIAL')], max_length=100)),
                ('in_stock', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('colour', models.CharField(blank=True, max_length=20, null=True)),
                ('length', models.CharField(blank=True, choices=[('SHORT SLEEVE', 'SHORT SLEEVE'), ('LONG SLEEVE', 'LONG SLEEVE')], max_length=20, null=True)),
                ('size', models.CharField(blank=True, choices=[('Small', 'Small'), ('Medium', 'Medium'), ('Large', 'Large'), ('Extra-Large', 'Extra-Large')], max_length=20, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('grade', models.CharField(blank=True, max_length=10, null=True)),
                ('quantity', models.IntegerField(default=1)),
                ('marker', models.BooleanField(default=False)),
                ('custom_text', models.CharField(blank=True, max_length=200, null=True)),
                ('ordered', models.BooleanField(default=False)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.item')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ref_code', models.CharField(blank=True, max_length=20, null=True)),
                ('ordered_date', models.DateTimeField(blank=True, null=True)),
                ('ordered', models.BooleanField(default=False)),
                ('closed', models.BooleanField(blank=True, default=False, null=True)),
                ('address', models.CharField(blank=True, max_length=1000, null=True)),
                ('payment_id', models.CharField(blank=True, max_length=20, null=True)),
                ('coupon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.coupon')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('items', models.ManyToManyField(related_name='item_in_order', to='store.orderitem')),
            ],
        ),
    ]
