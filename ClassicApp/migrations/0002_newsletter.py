# Generated by Django 4.0 on 2024-11-23 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ClassicApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Newsletter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
    ]
