# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alias',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hostname', models.CharField(max_length=256)),
                ('status', models.CharField(default='active', max_length=256)),
                ('description', models.TextField(default='', blank=True)),
                ('administrative_info', models.TextField(default='', help_text=b"Required if not a .ccnmtl.columbia.edu hostname.Please use this field for information about where the domain is registered, what account it's set up with (don't enter passwords here though) and who handles payments, DNS changes, etc.", blank=True)),
            ],
            options={
                'ordering': ['hostname'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AliasContact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('alias', models.ForeignKey(to='main.Alias')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('description', models.TextField(default='', blank=True)),
                ('graphite_name', models.CharField(default='', max_length=256, blank=True)),
                ('sentry_name', models.CharField(default='', max_length=256, blank=True)),
                ('pmt_id', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ApplicationAlias',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('alias', models.ForeignKey(to='main.Alias')),
                ('application', models.ForeignKey(to='main.Application')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ApplicationContact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('application', models.ForeignKey(to='main.Application')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('email', models.CharField(default=b'', max_length=256)),
                ('phone', models.CharField(default=b'', max_length=256)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='IPAddress',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ipv4', models.CharField(max_length=256)),
                ('mac_addr', models.CharField(max_length=256)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('details', models.TextField(default='', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OperatingSystem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('version', models.CharField(max_length=256)),
            ],
            options={
                'ordering': ['version'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OSFamily',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('primary_function', models.TextField(default='', blank=True)),
                ('virtual', models.BooleanField(default=False)),
                ('memory', models.CharField(max_length=256, blank=True)),
                ('disk', models.CharField(max_length=256, blank=True)),
                ('swap', models.CharField(max_length=256, blank=True)),
                ('notes', models.TextField(default='', blank=True)),
                ('deprecated', models.BooleanField(default=False)),
                ('graphite_name', models.CharField(default='', max_length=256, blank=True)),
                ('sentry_name', models.CharField(default='', max_length=256, blank=True)),
                ('location', models.ForeignKey(default=b'', to='main.Location', null=True)),
                ('operating_system', models.ForeignKey(to='main.OperatingSystem')),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ServerContact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('contact', models.ForeignKey(to='main.Contact')),
                ('server', models.ForeignKey(to='main.Server')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Technology',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VMLocation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dom_0', models.ForeignKey(related_name=b'dom_0', to='main.Server')),
                ('dom_u', models.ForeignKey(related_name=b'dom_u', to='main.Server')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterOrderWithRespectTo(
            name='servercontact',
            order_with_respect_to='server',
        ),
        migrations.AddField(
            model_name='operatingsystem',
            name='family',
            field=models.ForeignKey(to='main.OSFamily'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ipaddress',
            name='server',
            field=models.ForeignKey(to='main.Server'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='applicationcontact',
            name='contact',
            field=models.ForeignKey(to='main.Contact'),
            preserve_default=True,
        ),
        migrations.AlterOrderWithRespectTo(
            name='applicationcontact',
            order_with_respect_to='application',
        ),
        migrations.AddField(
            model_name='application',
            name='technology',
            field=models.ForeignKey(to='main.Technology', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='aliascontact',
            name='contact',
            field=models.ForeignKey(to='main.Contact'),
            preserve_default=True,
        ),
        migrations.AlterOrderWithRespectTo(
            name='aliascontact',
            order_with_respect_to='alias',
        ),
        migrations.AddField(
            model_name='alias',
            name='ip_address',
            field=models.ForeignKey(to='main.IPAddress', null=True),
            preserve_default=True,
        ),
    ]
