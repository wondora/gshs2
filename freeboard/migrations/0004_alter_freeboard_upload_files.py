# Generated by Django 4.1.1 on 2022-11-08 13:40

from django.db import migrations, models
import freeboard.models


class Migration(migrations.Migration):

    dependencies = [
        ('freeboard', '0003_alter_freeboard_upload_files'),
    ]

    operations = [
        migrations.AlterField(
            model_name='freeboard',
            name='upload_files',
            field=models.FileField(blank=True, null=True, upload_to=freeboard.models.get_file_path, verbose_name='파일'),
        ),
    ]
