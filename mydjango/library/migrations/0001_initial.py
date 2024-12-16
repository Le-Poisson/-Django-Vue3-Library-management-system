# Generated by Django 3.2.25 on 2024-12-06 01:50

from django.db import migrations, models
import django.db.models.deletion
import library.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Administrator',
            fields=[
                ('adminID', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('account', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('authorID', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('introduction', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Backgroud',
            fields=[
                ('backgroundID', models.AutoField(primary_key=True, serialize=False)),
                ('url', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Bookshelf',
            fields=[
                ('bookID', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('amount', models.IntegerField()),
                ('lend_amount', models.IntegerField()),
                ('introduction', models.TextField(null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.author')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('userID', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('phoneNum', models.CharField(max_length=20)),
                ('account', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('borrowTimes', models.IntegerField()),
                ('ovdTimes', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Reserve',
            fields=[
                ('reserveID', models.AutoField(primary_key=True, serialize=False)),
                ('startTime', models.DateTimeField(default=library.models.get_default_start_time)),
                ('DDL', models.DateTimeField(default=library.models.get_default_ddl)),
                ('endTime', models.DateTimeField(null=True)),
                ('bookID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.bookshelf')),
                ('userID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.user')),
            ],
        ),
        migrations.CreateModel(
            name='Quotation',
            fields=[
                ('quotationID', models.AutoField(primary_key=True, serialize=False)),
                ('quotation', models.TextField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.author')),
            ],
        ),
        migrations.CreateModel(
            name='Lend',
            fields=[
                ('lendID', models.AutoField(primary_key=True, serialize=False)),
                ('startTime', models.DateTimeField(default=library.models.get_default_start_time)),
                ('DDL', models.DateTimeField(default=library.models.get_default_ddl)),
                ('endTime', models.DateTimeField(null=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.bookshelf')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.user')),
            ],
        ),
    ]