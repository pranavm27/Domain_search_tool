# Generated by Django 2.1.1 on 2018-10-05 08:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('DWH_app', '0004_auto_20181005_1251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='searchresults',
            name='search_key',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='DWH_app.Searches', unique=True),
        ),
    ]
