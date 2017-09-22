# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-21 22:33
from __future__ import unicode_literals

from django.db import migrations, models
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('product_catalog', '0007_auto_20170919_0807'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='categories',
            field=models.ManyToManyField(blank=True, related_name='products', to='product_catalog.Category', verbose_name='categories'),
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=django_extensions.db.fields.AutoSlugField(blank=True, editable=False, max_length=255, populate_from=[b'title'], verbose_name='slug'),
        ),
    ]