# Generated by Django 2.0.5 on 2018-05-04 15:31

from django.db import migrations, models
import mainApp.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Correo Electronico')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='Nombre')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='Apellido')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Registro')),
                ('is_active', models.BooleanField(default=True, verbose_name='Activo')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatars/')),
                ('enabled', models.BooleanField(verbose_name='Habilitado')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name_plural': 'users',
                'verbose_name': 'user',
            },
            managers=[
                ('objects', mainApp.models.UserManager()),
            ],
        ),
    ]
