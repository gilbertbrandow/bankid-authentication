# Generated by Django 5.0.6 on 2024-06-17 19:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_alter_bankidauthentication_table'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bankidauthentication',
            name='is_active',
        ),
    ]