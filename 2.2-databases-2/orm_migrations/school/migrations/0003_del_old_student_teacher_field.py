# Generated by Django 4.1.4 on 2022-12-07 13:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0002_add_m2m_teachers_field'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='teacher',
        ),
    ]
