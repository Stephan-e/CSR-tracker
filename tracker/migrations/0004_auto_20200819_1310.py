# Generated by Django 3.0.5 on 2020-08-19 13:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0003_auto_20200819_1304'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='land_saved_use',
            new_name='land_use',
        ),
        migrations.RenameField(
            model_name='recipe',
            old_name='land_saved_use_veg',
            new_name='land_use_veg',
        ),
    ]
