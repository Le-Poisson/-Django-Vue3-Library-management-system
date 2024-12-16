# Generated by Django 3.2.25 on 2024-12-08 03:36

from django.db import migrations, models
import django.db.models.deletion
import library.models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_lend_reserveid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('messageID', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.TextField()),
                ('time', models.DateTimeField(default=library.models.get_default_start_time)),
                ('isRead', models.BooleanField(default=False)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to='library.user')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to='library.administrator')),
            ],
        ),
    ]
