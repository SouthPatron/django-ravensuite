# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
		db.rename_table( 'common_userpermissions', 'common_userpermission' )

    def backwards(self, orm):
		db.rename_table( 'common_userpermission', 'common_userpermissions' )

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
        'common.account': {
            'Meta': {'object_name': 'Account'},
            'balance': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'client': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['common.Client']", 'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'transaction_no': ('django.db.models.fields.BigIntegerField', [], {'default': '1'})
        },
        'common.accounttransaction': {
            'Meta': {'ordering': "[u'-event_time', u'-creation_time']", 'object_name': 'AccountTransaction'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Account']"}),
            'amount': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'balance_after': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'balance_before': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'creation_time': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'event_time': ('django.db.models.fields.DateTimeField', [], {}),
            'group': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'refnum': ('django.db.models.fields.BigIntegerField', [], {'default': '1'}),
            'source_document': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.SourceDocument']"})
        },
        'common.accounttransactiondata': {
            'Meta': {'object_name': 'AccountTransactionData'},
            'account_transaction': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['common.AccountTransaction']", 'unique': 'True'}),
            'data': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'common.activity': {
            'Meta': {'object_name': 'Activity'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Organization']"})
        },
        'common.authenticationcode': {
            'Meta': {'object_name': 'AuthenticationCode'},
            'authentication_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '16', 'blank': 'True'}),
            'creation_time': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'common.client': {
            'Meta': {'object_name': 'Client'},
            'email_address': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '256', 'blank': 'True'}),
            'fax_number': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '64', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Organization']"}),
            'physical_address': ('django.db.models.fields.TextField', [], {'default': "u''", 'blank': 'True'}),
            'postal_address': ('django.db.models.fields.TextField', [], {'default': "u''", 'blank': 'True'}),
            'refnum': ('django.db.models.fields.BigIntegerField', [], {}),
            'telephone_number': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '64', 'blank': 'True'}),
            'trading_name': ('django.db.models.fields.CharField', [], {'max_length': '192'})
        },
        'common.debugcontrol': {
            'Meta': {'object_name': 'DebugControl'},
            'current_time': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'common.organization': {
            'Meta': {'object_name': 'Organization'},
            'email_address': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '256', 'blank': 'True'}),
            'fax_number': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '64', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'physical_address': ('django.db.models.fields.TextField', [], {'default': "u''", 'blank': 'True'}),
            'postal_address': ('django.db.models.fields.TextField', [], {'default': "u''", 'blank': 'True'}),
            'refnum': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True'}),
            'telephone_number': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '64', 'blank': 'True'}),
            'trading_name': ('django.db.models.fields.CharField', [], {'max_length': '192'})
        },
        'common.organizationaccount': {
            'Meta': {'object_name': 'OrganizationAccount'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organization': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['common.Organization']", 'unique': 'True'})
        },
        'common.organizationcounter': {
            'Meta': {'object_name': 'OrganizationCounter'},
            'client_no': ('django.db.models.fields.BigIntegerField', [], {'default': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organization': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['common.Organization']", 'unique': 'True'}),
            'project_no': ('django.db.models.fields.BigIntegerField', [], {'default': '1'}),
            'source_document_no': ('django.db.models.fields.BigIntegerField', [], {'default': '1'})
        },
        'common.project': {
            'Meta': {'object_name': 'Project'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Client']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'refnum': ('django.db.models.fields.BigIntegerField', [], {}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'common.sourcedocument': {
            'Meta': {'ordering': "[u'-event_time']", 'object_name': 'SourceDocument'},
            'allocated': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'amount': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Client']"}),
            'creation_time': ('django.db.models.fields.DateTimeField', [], {}),
            'document_state': ('django.db.models.fields.IntegerField', [], {}),
            'document_type': ('django.db.models.fields.IntegerField', [], {}),
            'event_time': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'refnum': ('django.db.models.fields.BigIntegerField', [], {}),
            'tax': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'total': ('django.db.models.fields.BigIntegerField', [], {'default': '0'})
        },
        'common.sourcedocumentallocation': {
            'Meta': {'object_name': 'SourceDocumentAllocation'},
            'amount': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'destination': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'destination_allocation'", 'to': "orm['common.SourceDocument']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'source_allocation'", 'to': "orm['common.SourceDocument']"})
        },
        'common.sourcedocumentline': {
            'Meta': {'object_name': 'SourceDocumentLine'},
            'amount': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'perunit': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'source_document': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.SourceDocument']"}),
            'tax_amount': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'tax_rate': ('django.db.models.fields.IntegerField', [], {}),
            'total': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'units': ('django.db.models.fields.BigIntegerField', [], {'default': '0'})
        },
        'common.sourcedocumentmeta': {
            'Meta': {'object_name': 'SourceDocumentMeta'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'source_document': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.SourceDocument']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'common.systemcounter': {
            'Meta': {'object_name': 'SystemCounter'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organization_no': ('django.db.models.fields.BigIntegerField', [], {'default': '1'}),
            'profile_no': ('django.db.models.fields.BigIntegerField', [], {'default': '1'})
        },
        'common.task': {
            'Meta': {'object_name': 'Task'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Activity']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'common.timesheetentry': {
            'Meta': {'ordering': "[u'-start_time']", 'object_name': 'TimesheetEntry'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Project']"}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Task']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'common.timesheettimer': {
            'Meta': {'ordering': "[u'-start_time']", 'object_name': 'TimesheetTimer'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Project']"}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Task']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'common.usermembership': {
            'Meta': {'object_name': 'UserMembership'},
            'category': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Organization']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'common.userpermission': {
            'Meta': {'object_name': 'UserPermission'},
            'crud': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '255'}),
            'entity': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'refnum': ('django.db.models.fields.BigIntegerField', [], {}),
            'user_membership': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.UserMembership']"})
        },
        'common.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'creation_time': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_seen': ('django.db.models.fields.DateTimeField', [], {}),
            'refnum': ('django.db.models.fields.BigIntegerField', [], {}),
            'state': ('django.db.models.fields.CharField', [], {'default': "u'unauthenticated'", 'max_length': '16'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['common']
