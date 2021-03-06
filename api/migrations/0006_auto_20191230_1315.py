# Generated by Django 3.0.1 on 2019-12-30 12:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_sprava'),
    ]

    operations = [
        migrations.CreateModel(
            name='Miestnost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazov', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=1200)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('miestnost', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='miestnost', to='api.Miestnost')),
                ('odosielatel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='odosielatelPost', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('timestamp',),
            },
        ),
        migrations.RemoveField(
            model_name='produkt',
            name='kategoria',
        ),
        migrations.RenameField(
            model_name='sprava',
            old_name='message',
            new_name='sprava',
        ),
        migrations.RemoveField(
            model_name='sprava',
            name='is_read',
        ),
        migrations.RemoveField(
            model_name='sprava',
            name='receiver',
        ),
        migrations.RemoveField(
            model_name='sprava',
            name='sender',
        ),
        migrations.AddField(
            model_name='sprava',
            name='odosielatel',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='odosielatel', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sprava',
            name='prijmatel',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='prijmatel', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Kategoria',
        ),
        migrations.DeleteModel(
            name='Produkt',
        ),
    ]
