# Generated by Django 4.1.1 on 2022-11-14 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freeboard', '0006_delete_free_freeboard_comments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='freeboard',
            name='registered_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='등록시간'),
        ),
    ]
