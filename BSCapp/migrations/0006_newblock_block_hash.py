# Generated by Django 2.0 on 2018-07-09 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BSCapp', '0005_delete_checklog'),
    ]

    operations = [
        migrations.AddField(
            model_name='newblock',
            name='block_hash',
            field=models.CharField(default='', max_length=64),
        ),
    ]
