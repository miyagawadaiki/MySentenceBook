# Generated by Django 2.2.3 on 2019-07-07 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sentences', '0002_auto_20190706_1548'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='is_public',
            field=models.BooleanField(default=False, verbose_name='Go Publish'),
        ),
    ]