# Generated by Django 5.0.4 on 2024-04-04 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_management', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='company_code',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]