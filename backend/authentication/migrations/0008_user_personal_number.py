# Generated by Django 5.0.6 on 2024-07-19 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0007_alter_account_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='personal_number',
            field=models.CharField(default=199001012385, max_length=255, unique=True),
            preserve_default=False,
        ),
    ]