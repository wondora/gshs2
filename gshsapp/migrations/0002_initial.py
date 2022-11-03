# Generated by Django 4.1.1 on 2022-11-03 12:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('gshsapp', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='gigiinfo',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='gigiinfo', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='change_photo',
            name='replacement',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='change_photo', to='gshsapp.replacement'),
        ),
        migrations.AddField(
            model_name='buyproduct',
            name='gubun',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buyproduct', to='gshsapp.gubun'),
        ),
    ]
