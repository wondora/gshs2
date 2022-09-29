# Generated by Django 4.1.1 on 2022-09-29 09:17

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('password', models.CharField(blank=True, max_length=100, null=True)),
                ('username', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('email', models.CharField(blank=True, max_length=50, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=50)),
                ('subject', models.CharField(max_length=50, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Buyproduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(max_length=20)),
                ('model', models.CharField(max_length=30)),
                ('bigo', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Freeboard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Gigiinfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=20)),
                ('color', models.BooleanField(default=False)),
                ('jaego', models.BooleanField(default=False)),
                ('notuse', models.BooleanField(default=False)),
                ('bigo', models.CharField(max_length=100, null=True)),
                ('buyproduct', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gigiinfo', to='gshsapp.buyproduct')),
            ],
        ),
        migrations.CreateModel(
            name='Gubun',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gubun', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('building', models.CharField(max_length=50)),
                ('hosil', models.CharField(max_length=20)),
                ('lcategory', models.CharField(max_length=20)),
                ('bigo', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Memo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Replacement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('bigo', models.CharField(max_length=100, null=True)),
                ('gigiinfo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replacement', to='gshsapp.gigiinfo')),
                ('gubun', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replacement', to='gshsapp.gubun')),
            ],
        ),
        migrations.CreateModel(
            name='Repair',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('problem', models.CharField(max_length=50)),
                ('result', models.CharField(max_length=50)),
                ('bigo', models.CharField(max_length=100, null=True)),
                ('gigiinfo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='repair', to='gshsapp.gigiinfo')),
            ],
        ),
        migrations.AddField(
            model_name='gigiinfo',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gigiinfo', to='gshsapp.location'),
        ),
        migrations.AddField(
            model_name='gigiinfo',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gigiinfo', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='buyproduct',
            name='gubun',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buyproduct', to='gshsapp.gubun'),
        ),
    ]
