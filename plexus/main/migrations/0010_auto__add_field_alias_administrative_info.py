# flake8: noqa
# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Alias.administrative_info'
        db.add_column(u'main_alias', 'administrative_info',
                      self.gf('django.db.models.fields.TextField')(default=u'', blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Alias.administrative_info'
        db.delete_column(u'main_alias', 'administrative_info')


    models = {
        u'main.alias': {
            'Meta': {'ordering': "['hostname']", 'object_name': 'Alias'},
            'administrative_info': ('django.db.models.fields.TextField', [], {'default': "u''", 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "u''", 'blank': 'True'}),
            'hostname': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.IPAddress']", 'null': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "u'active'", 'max_length': '256'})
        },
        u'main.aliascontact': {
            'Meta': {'ordering': "(u'_order',)", 'object_name': 'AliasContact'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'alias': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Alias']"}),
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Contact']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'main.application': {
            'Meta': {'ordering': "['name']", 'object_name': 'Application'},
            'description': ('django.db.models.fields.TextField', [], {'default': "u''", 'blank': 'True'}),
            'graphite_name': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '256', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'pmt_id': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'sentry_name': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '256', 'blank': 'True'}),
            'technology': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Technology']", 'null': 'True'})
        },
        u'main.applicationalias': {
            'Meta': {'object_name': 'ApplicationAlias'},
            'alias': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Alias']"}),
            'application': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Application']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'main.applicationcontact': {
            'Meta': {'ordering': "(u'_order',)", 'object_name': 'ApplicationContact'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'application': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Application']"}),
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Contact']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'main.contact': {
            'Meta': {'object_name': 'Contact'},
            'email': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'phone': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256'})
        },
        u'main.ipaddress': {
            'Meta': {'object_name': 'IPAddress'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ipv4': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'mac_addr': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'server': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Server']"})
        },
        u'main.location': {
            'Meta': {'object_name': 'Location'},
            'details': ('django.db.models.fields.TextField', [], {'default': "u''", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'main.operatingsystem': {
            'Meta': {'ordering': "['version']", 'object_name': 'OperatingSystem'},
            'family': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.OSFamily']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'main.osfamily': {
            'Meta': {'ordering': "['name']", 'object_name': 'OSFamily'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'main.server': {
            'Meta': {'ordering': "['name']", 'object_name': 'Server'},
            'deprecated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'disk': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'graphite_name': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '256', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'to': u"orm['main.Location']", 'null': 'True'}),
            'memory': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'munin_name': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '256', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'notes': ('django.db.models.fields.TextField', [], {'default': "u''", 'blank': 'True'}),
            'operating_system': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.OperatingSystem']"}),
            'primary_function': ('django.db.models.fields.TextField', [], {'default': "u''", 'blank': 'True'}),
            'sentry_name': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '256', 'blank': 'True'}),
            'swap': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'virtual': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'main.servercontact': {
            'Meta': {'ordering': "(u'_order',)", 'object_name': 'ServerContact'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Contact']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'server': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Server']"})
        },
        u'main.technology': {
            'Meta': {'object_name': 'Technology'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'main.vmlocation': {
            'Meta': {'object_name': 'VMLocation'},
            'dom_0': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'dom_0'", 'to': u"orm['main.Server']"}),
            'dom_u': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'dom_u'", 'to': u"orm['main.Server']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['main']
