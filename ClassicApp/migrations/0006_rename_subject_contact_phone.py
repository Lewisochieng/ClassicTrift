# Generated by Django 4.0 on 2024-12-03 08:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ClassicApp', '0005_remove_product_category_delete_category_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contact',
            old_name='subject',
            new_name='phone',
        ),
    ]
