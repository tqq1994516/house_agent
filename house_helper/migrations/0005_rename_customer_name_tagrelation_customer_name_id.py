# Generated by Django 3.2.3 on 2021-06-15 15:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('house_helper', '0004_rename_type_tag_type_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tagrelation',
            old_name='customer_name',
            new_name='customer_name_id',
        ),
    ]