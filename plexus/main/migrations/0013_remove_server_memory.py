# Generated by Django 3.2.12 on 2022-04-06 15:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_auto_20220325_1331'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='server',
            name='memory',
        ),
    ]
