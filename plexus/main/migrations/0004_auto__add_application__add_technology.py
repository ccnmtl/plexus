# flake8: noqa
# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Application'
        db.create_table('main_application', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('description', self.gf('django.db.models.fields.TextField')(default=u'', blank=True)),
            ('technology', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Technology'], null=True)),
            ('graphite_name', self.gf('django.db.models.fields.CharField')(default=u'', max_length=256, blank=True)),
            ('pmt_id', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('main', ['Application'])

        # Adding model 'Technology'
        db.create_table('main_technology', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal('main', ['Technology'])


    def backwards(self, orm):
        # Deleting model 'Application'
        db.delete_table('main_application')

        # Deleting model 'Technology'
        db.delete_table('main_technology')


    models = {
        'main.alias': {
            'Meta': {'object_name': 'Alias'},
            'description': ('django.db.models.fields.TextField', [], {'default': "u''", 'blank': 'True'}),
            'hostname': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.IPAddress']", 'null': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "u'active'", 'max_length': '256'})
        },
        'main.aliascontact': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'AliasContact'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'alias': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Alias']"}),
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Contact']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'main.application': {
            'Meta': {'object_name': 'Application'},
            'description': ('django.db.models.fields.TextField', [], {'default': "u''", 'blank': 'True'}),
            'graphite_name': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '256', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'pmt_id': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'technology': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Technology']", 'null': 'True'})
        },
        'main.contact': {
            'Meta': {'object_name': 'Contact'},
            'email': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'phone': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256'})
        },
        'main.ipaddress': {
            'Meta': {'object_name': 'IPAddress'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ipv4': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'mac_addr': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'server': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Server']"})
        },
        'main.location': {
            'Meta': {'object_name': 'Location'},
            'details': ('django.db.models.fields.TextField', [], {'default': "u''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'main.operatingsystem': {
            'Meta': {'object_name': 'OperatingSystem'},
            'family': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.OSFamily']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'main.osfamily': {
            'Meta': {'object_name': 'OSFamily'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'main.server': {
            'Meta': {'object_name': 'Server'},
            'deprecated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'disk': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'graphite_name': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '256', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'to': "orm['main.Location']", 'null': 'True'}),
            'memory': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'notes': ('django.db.models.fields.TextField', [], {'default': "u''", 'blank': 'True'}),
            'operating_system': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.OperatingSystem']"}),
            'primary_function': ('django.db.models.fields.TextField', [], {'default': "u''", 'blank': 'True'}),
            'swap': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'virtual': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'main.technology': {
            'Meta': {'object_name': 'Technology'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'main.vmlocation': {
            'Meta': {'object_name': 'VMLocation'},
            'dom_0': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'dom_0'", 'to': "orm['main.Server']"}),
            'dom_u': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'dom_u'", 'to': "orm['main.Server']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['main']
