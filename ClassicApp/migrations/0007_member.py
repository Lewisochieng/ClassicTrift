# Generated by Django 4.0 on 2024-12-03 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ClassicApp', '0006_rename_subject_contact_phone'),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
            ],
        ),
    ]
