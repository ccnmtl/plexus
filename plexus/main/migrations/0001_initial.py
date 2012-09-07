# flake8: noqa
# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Location'
        db.create_table('main_location', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('details', self.gf('django.db.models.fields.TextField')(default=u'', blank=True)),
        ))
        db.send_create_signal('main', ['Location'])

        # Adding model 'OSFamily'
        db.create_table('main_osfamily', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal('main', ['OSFamily'])

        # Adding model 'OperatingSystem'
        db.create_table('main_operatingsystem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('family', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.OSFamily'])),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal('main', ['OperatingSystem'])

        # Adding model 'Server'
        db.create_table('main_server', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('primary_function', self.gf('django.db.models.fields.TextField')(default=u'', blank=True)),
            ('virtual', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Location'])),
            ('operating_system', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.OperatingSystem'])),
            ('memory', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('disk', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('swap', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('notes', self.gf('django.db.models.fields.TextField')(default=u'', blank=True)),
            ('deprecated', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('main', ['Server'])

        # Adding model 'IPAddress'
        db.create_table('main_ipaddress', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ipv4', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('mac_addr', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('server', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Server'])),
        ))
        db.send_create_signal('main', ['IPAddress'])

        # Adding model 'VMLocation'
        db.create_table('main_vmlocation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dom_u', self.gf('django.db.models.fields.related.ForeignKey')(related_name='dom_u', to=orm['main.Server'])),
            ('dom_0', self.gf('django.db.models.fields.related.ForeignKey')(related_name='dom_0', to=orm['main.Server'])),
        ))
        db.send_create_signal('main', ['VMLocation'])

        # Adding model 'Contact'
        db.create_table('main_contact', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal('main', ['Contact'])

        # Adding model 'Alias'
        db.create_table('main_alias', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('hostname', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('ip_address', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.IPAddress'], null=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default=u'active', max_length=256)),
            ('description', self.gf('django.db.models.fields.TextField')(default=u'', blank=True)),
        ))
        db.send_create_signal('main', ['Alias'])

        # Adding model 'AliasContact'
        db.create_table('main_aliascontact', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('alias', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Alias'])),
            ('contact', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Contact'])),
            ('_order', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('main', ['AliasContact'])


    def backwards(self, orm):
        # Deleting model 'Location'
        db.delete_table('main_location')

        # Deleting model 'OSFamily'
        db.delete_table('main_osfamily')

        # Deleting model 'OperatingSystem'
        db.delete_table('main_operatingsystem')

        # Deleting model 'Server'
        db.delete_table('main_server')

        # Deleting model 'IPAddress'
        db.delete_table('main_ipaddress')

        # Deleting model 'VMLocation'
        db.delete_table('main_vmlocation')

        # Deleting model 'Contact'
        db.delete_table('main_contact')

        # Deleting model 'Alias'
        db.delete_table('main_alias')

        # Deleting model 'AliasContact'
        db.delete_table('main_aliascontact')


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
        'main.contact': {
            'Meta': {'object_name': 'Contact'},
            'email': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '256'})
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
            'disk': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Location']"}),
            'memory': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'notes': ('django.db.models.fields.TextField', [], {'default': "u''", 'blank': 'True'}),
            'operating_system': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.OperatingSystem']"}),
            'primary_function': ('django.db.models.fields.TextField', [], {'default': "u''", 'blank': 'True'}),
            'swap': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'virtual': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'main.vmlocation': {
            'Meta': {'object_name': 'VMLocation'},
            'dom_0': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'dom_0'", 'to': "orm['main.Server']"}),
            'dom_u': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'dom_u'", 'to': "orm['main.Server']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['main']
