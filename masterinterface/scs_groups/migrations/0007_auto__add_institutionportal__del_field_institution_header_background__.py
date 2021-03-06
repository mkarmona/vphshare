# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'InstitutionPortal'
        db.create_table('scs_groups_institutionportal', (
            ('institution', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['scs_groups.Institution'], unique=True, primary_key=True)),
            ('subdomain', self.gf('django.db.models.fields.CharField')(unique=True, max_length=16)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('background', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('header_background', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
        ))
        db.send_create_signal('scs_groups', ['InstitutionPortal'])

        # Deleting field 'Institution.header_background'
        db.delete_column('scs_groups_institution', 'header_background')

        # Deleting field 'Institution.subdomain'
        db.delete_column('scs_groups_institution', 'subdomain')

        # Deleting field 'Institution.background'
        db.delete_column('scs_groups_institution', 'background')

        # Deleting field 'Institution.subdomain_name'
        db.delete_column('scs_groups_institution', 'subdomain_name')


    def backwards(self, orm):
        # Deleting model 'InstitutionPortal'
        db.delete_table('scs_groups_institutionportal')

        # Adding field 'Institution.header_background'
        db.add_column('scs_groups_institution', 'header_background',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=64, blank=True),
                      keep_default=False)

        # Adding field 'Institution.subdomain'
        db.add_column('scs_groups_institution', 'subdomain',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=16, blank=True),
                      keep_default=False)

        # Adding field 'Institution.background'
        db.add_column('scs_groups_institution', 'background',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=64, blank=True),
                      keep_default=False)

        # Adding field 'Institution.subdomain_name'
        db.add_column('scs_groups_institution', 'subdomain_name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=64, blank=True),
                      keep_default=False)


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'scs_groups.auditlog': {
            'Meta': {'object_name': 'AuditLog'},
            'date': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'log': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        },
        'scs_groups.institution': {
            'Meta': {'ordering': "['name']", 'object_name': 'Institution', '_ormbases': ['scs_groups.VPHShareSmartGroup']},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'admin_address': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'admin_email': ('django.db.models.fields.EmailField', [], {'max_length': '64'}),
            'admin_fullname': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'admin_phone': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'breach_address': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'breach_email': ('django.db.models.fields.EmailField', [], {'max_length': '64', 'blank': 'True'}),
            'breach_fullname': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'breach_phone': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'formal_address': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'formal_email': ('django.db.models.fields.EmailField', [], {'max_length': '64', 'blank': 'True'}),
            'formal_fullname': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'formal_phone': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'policies_url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'blank': 'True'}),
            'signed_dsa': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'vphsharesmartgroup_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['scs_groups.VPHShareSmartGroup']", 'unique': 'True', 'primary_key': 'True'})
        },
        'scs_groups.institutionportal': {
            'Meta': {'object_name': 'InstitutionPortal'},
            'background': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'header_background': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'institution': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['scs_groups.Institution']", 'unique': 'True', 'primary_key': 'True'}),
            'subdomain': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '16'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'scs_groups.study': {
            'Meta': {'ordering': "['name']", 'object_name': 'Study', '_ormbases': ['scs_groups.VPHShareSmartGroup']},
            'finish_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'institution': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scs_groups.Institution']"}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'vphsharesmartgroup_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['scs_groups.VPHShareSmartGroup']", 'unique': 'True', 'primary_key': 'True'})
        },
        'scs_groups.subscriptionrequest': {
            'Meta': {'object_name': 'SubscriptionRequest'},
            'date': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'scs_groups.vphsharesmartgroup': {
            'Meta': {'ordering': "['name']", 'object_name': 'VPHShareSmartGroup', '_ormbases': ['auth.Group']},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'group_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.Group']", 'unique': 'True', 'primary_key': 'True'}),
            'managers': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['auth.Group']"})
        }
    }

    complete_apps = ['scs_groups']