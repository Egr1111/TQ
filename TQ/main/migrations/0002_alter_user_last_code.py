# Generated by Django 4.2.4 on 2023-08-22 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='last_code',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Время последнего сообщения'),
        ),
    ]
