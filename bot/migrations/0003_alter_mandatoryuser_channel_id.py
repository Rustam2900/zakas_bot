# Generated by Django 5.0 on 2024-08-04 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0002_alter_namerole_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mandatoryuser',
            name='channel_id',
            field=models.IntegerField(unique=True),
        ),
    ]
