# Generated by Django 3.0.1 on 2019-12-30 12:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20191230_1315'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='message',
            new_name='sprava',
        ),
    ]