# Generated by Django 3.2.3 on 2021-06-15 14:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('house_helper', '0003_auto_20210615_1058'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tag',
            old_name='type',
            new_name='type_id',
        ),
    ]