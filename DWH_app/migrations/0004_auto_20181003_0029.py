# Generated by Django 2.1.1 on 2018-10-02 18:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('DWH_app', '0003_campaigns'),
    ]

    operations = [
        migrations.RenameField(
            model_name='campaigns',
            old_name='cmapaign_type',
            new_name='campaign_type',
        ),
    ]
