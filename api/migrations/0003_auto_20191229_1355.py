# Generated by Django 3.0.1 on 2019-12-29 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20191229_1349'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='produkt',
            name='owner',
        ),
        migrations.AlterField(
            model_name='pouzivatelprofil',
            name='title',
            field=models.CharField(blank=True, max_length=5),
        ),
    ]