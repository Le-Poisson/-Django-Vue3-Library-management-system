# Generated by Django 3.2.25 on 2024-12-06 02:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lend',
            name='reserveID',
            field=models.IntegerField(null=True),
        ),
    ]
