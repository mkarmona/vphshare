# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'EJob.owner_name'
        db.add_column('cilab_ejobs_ejob', 'owner_name',
                      self.gf('django.db.models.fields.CharField')(default=False, max_length=128),
                      keep_default=False)

        # Adding field 'EJob.worker_name'
        db.add_column('cilab_ejobs_ejob', 'worker_name',
                      self.gf('django.db.models.fields.BigIntegerField')(default=False, max_length=128),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'EJob.owner_name'
        db.delete_column('cilab_ejobs_ejob', 'owner_name')

        # Deleting field 'EJob.worker_name'
        db.delete_column('cilab_ejobs_ejob', 'worker_name')


    models = {
        'cilab_ejobs.ejob': {
            'Meta': {'object_name': 'EJob'},
            'auto_run': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'creation_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'input_data': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '4096'}),
            'message': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1024'}),
            'modification_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'output_data': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '4096'}),
            'owner_id': ('django.db.models.fields.BigIntegerField', [], {}),
            'owner_name': ('django.db.models.fields.CharField', [], {'default': 'False', 'max_length': '128'}),
            'state': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'worker_id': ('django.db.models.fields.BigIntegerField', [], {}),
            'worker_name': ('django.db.models.fields.BigIntegerField', [], {'default': 'False', 'max_length': '128'})
        }
    }

    complete_apps = ['cilab_ejobs']