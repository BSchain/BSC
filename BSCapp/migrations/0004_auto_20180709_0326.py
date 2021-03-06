# Generated by Django 2.0 on 2018-07-09 03:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BSCapp', '0003_auto_20180709_0305'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewBlock',
            fields=[
                ('block_height', models.IntegerField(primary_key=True, serialize=False)),
                ('prev_hash', models.CharField(max_length=64)),
                ('tx_id', models.CharField(default='', max_length=64)),
                ('block_timestamp', models.CharField(max_length=64)),
                ('nonce', models.CharField(max_length=64)),
            ],
        ),
        migrations.RemoveField(
            model_name='operationlog',
            name='block_height',
        ),
        migrations.RemoveField(
            model_name='operationlog',
            name='block_timestamp',
        ),
        migrations.RemoveField(
            model_name='operationlog',
            name='nonce',
        ),
        migrations.RemoveField(
            model_name='operationlog',
            name='prev_hash',
        ),
    ]
