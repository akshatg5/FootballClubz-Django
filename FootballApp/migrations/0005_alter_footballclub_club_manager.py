# Generated by Django 4.2.5 on 2023-09-24 20:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('FootballApp', '0004_alter_player_football_club'),
    ]

    operations = [
        migrations.AlterField(
            model_name='footballclub',
            name='club_manager',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clubs_managed', to=settings.AUTH_USER_MODEL),
        ),
    ]
