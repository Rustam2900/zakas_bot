# Generated by Django 5.0 on 2024-08-06 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0004_video'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderVideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('url', models.URLField()),
            ],
        ),
    ]
