# Generated by Django 3.2.12 on 2022-03-25 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grainlog', '0002_auto_20160324_0720'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grainlog',
            name='payload',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='grainlog',
            name='sha1',
            field=models.TextField(blank=True, db_index=True, default=''),
        ),
    ]
