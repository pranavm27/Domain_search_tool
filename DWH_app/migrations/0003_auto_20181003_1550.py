# Generated by Django 2.1.1 on 2018-10-03 10:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('DWH_app', '0002_auto_20181003_1547'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campaigns',
            name='user_id',
        ),
        migrations.AddField(
            model_name='campaigns',
            name='belongs_to',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]