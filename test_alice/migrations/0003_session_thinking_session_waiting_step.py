# Generated by Django 5.2 on 2025-04-20 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_alice', '0002_alter_session_is_open'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='thinking',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='session',
            name='waiting_step',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
