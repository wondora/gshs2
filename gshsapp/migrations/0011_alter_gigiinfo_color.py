# Generated by Django 4.1.1 on 2022-10-05 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gshsapp', '0010_alter_gigiinfo_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gigiinfo',
            name='color',
            field=models.CharField(blank=True, default='블랙', max_length=10),
        ),
    ]