# Generated by Django 4.1.4 on 2022-12-14 20:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('measurement', '0002_add_updated_at_field'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='measurement',
            name='updated_at',
        ),
    ]
