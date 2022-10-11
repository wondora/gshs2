# Generated by Django 4.1.1 on 2022-10-11 11:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gshsapp', '0013_location_locationgubun'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='repair',
            name='image',
        ),
        migrations.RemoveField(
            model_name='replacement',
            name='image',
        ),
        migrations.CreateModel(
            name='Repair_Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/%Y/%m/%d/')),
                ('repair', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='Repair_Photo', to='gshsapp.repair')),
            ],
        ),
        migrations.CreateModel(
            name='Change_Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/%Y/%m/%d/')),
                ('replacement', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='Change_Photo', to='gshsapp.replacement')),
            ],
        ),
    ]
