# Generated by Django 4.1.4 on 2022-12-23 08:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('advertisements', '0003_advertisement_draft_adv'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='advertisement',
            name='draft_adv',
        ),
    ]