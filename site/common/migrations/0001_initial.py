# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'DebugControl'
        db.create_table('common_debugcontrol', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('current_time', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('common', ['DebugControl'])

        # Adding model 'UserProfile'
        db.create_table('common_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('refnum', self.gf('django.db.models.fields.BigIntegerField')()),
            ('state', self.gf('django.db.models.fields.CharField')(default=u'unauthenticated', max_length=16)),
            ('creation_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('last_seen', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('common', ['UserProfile'])

        # Adding model 'AuthenticationCode'
        db.create_table('common_authenticationcode', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('creation_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('authentication_code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=16, blank=True)),
        ))
        db.send_create_signal('common', ['AuthenticationCode'])

        # Adding model 'SystemCounter'
        db.create_table('common_systemcounter', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('profile_no', self.gf('django.db.models.fields.BigIntegerField')(default=1)),
            ('organization_no', self.gf('django.db.models.fields.BigIntegerField')(default=1)),
        ))
        db.send_create_signal('common', ['SystemCounter'])

        # Adding model 'Organization'
        db.create_table('common_organization', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('trading_name', self.gf('django.db.models.fields.CharField')(max_length=192)),
            ('refnum', self.gf('django.db.models.fields.BigIntegerField')(unique=True)),
        ))
        db.send_create_signal('common', ['Organization'])

        # Adding model 'OrganizationAccount'
        db.create_table('common_organizationaccount', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('organization', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['common.Organization'], unique=True)),
        ))
        db.send_create_signal('common', ['OrganizationAccount'])

        # Adding model 'OrganizationCounter'
        db.create_table('common_organizationcounter', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('organization', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['common.Organization'], unique=True)),
            ('source_document_no', self.gf('django.db.models.fields.BigIntegerField')(default=1)),
            ('client_no', self.gf('django.db.models.fields.BigIntegerField')(default=1)),
            ('project_no', self.gf('django.db.models.fields.BigIntegerField')(default=1)),
        ))
        db.send_create_signal('common', ['OrganizationCounter'])

        # Adding model 'UserMembership'
        db.create_table('common_usermembership', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Organization'])),
            ('category', self.gf('django.db.models.fields.IntegerField')()),
            ('is_enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('common', ['UserMembership'])

        # Adding model 'UserPermissions'
        db.create_table('common_userpermissions', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_membership', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.UserMembership'])),
            ('entity', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('refnum', self.gf('django.db.models.fields.BigIntegerField')()),
            ('crud', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=255)),
        ))
        db.send_create_signal('common', ['UserPermissions'])

        # Adding model 'Client'
        db.create_table('common_client', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Organization'])),
            ('refnum', self.gf('django.db.models.fields.BigIntegerField')()),
            ('trading_name', self.gf('django.db.models.fields.CharField')(max_length=192)),
        ))
        db.send_create_signal('common', ['Client'])

        # Adding model 'SourceDocument'
        db.create_table('common_sourcedocument', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Client'])),
            ('refnum', self.gf('django.db.models.fields.BigIntegerField')()),
            ('creation_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('event_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('document_type', self.gf('django.db.models.fields.IntegerField')()),
            ('document_state', self.gf('django.db.models.fields.IntegerField')()),
            ('amount', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('tax', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('total', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('allocated', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
        ))
        db.send_create_signal('common', ['SourceDocument'])

        # Adding model 'SourceDocumentMeta'
        db.create_table('common_sourcedocumentmeta', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source_document', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.SourceDocument'])),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('common', ['SourceDocumentMeta'])

        # Adding model 'SourceDocumentLine'
        db.create_table('common_sourcedocumentline', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source_document', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.SourceDocument'])),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('units', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('perunit', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('amount', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('tax_rate', self.gf('django.db.models.fields.IntegerField')()),
            ('tax_amount', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('total', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
        ))
        db.send_create_signal('common', ['SourceDocumentLine'])

        # Adding model 'SourceDocumentAllocation'
        db.create_table('common_sourcedocumentallocation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'source_allocation', to=orm['common.SourceDocument'])),
            ('destination', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'destination_allocation', to=orm['common.SourceDocument'])),
            ('amount', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
        ))
        db.send_create_signal('common', ['SourceDocumentAllocation'])

        # Adding model 'Account'
        db.create_table('common_account', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('client', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['common.Client'], unique=True)),
            ('transaction_no', self.gf('django.db.models.fields.BigIntegerField')(default=1)),
            ('balance', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
        ))
        db.send_create_signal('common', ['Account'])

        # Adding model 'AccountTransaction'
        db.create_table('common_accounttransaction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Account'])),
            ('refnum', self.gf('django.db.models.fields.BigIntegerField')(default=1)),
            ('creation_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('event_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('group', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('balance_before', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('balance_after', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('amount', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('source_document', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.SourceDocument'])),
        ))
        db.send_create_signal('common', ['AccountTransaction'])

        # Adding model 'AccountTransactionData'
        db.create_table('common_accounttransactiondata', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('account_transaction', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['common.AccountTransaction'], unique=True)),
            ('data', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('common', ['AccountTransactionData'])

        # Adding model 'Activity'
        db.create_table('common_activity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Organization'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('common', ['Activity'])

        # Adding model 'Task'
        db.create_table('common_task', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('activity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Activity'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('common', ['Task'])

        # Adding model 'Project'
        db.create_table('common_project', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Client'])),
            ('refnum', self.gf('django.db.models.fields.BigIntegerField')()),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('common', ['Project'])

        # Adding model 'TimesheetEntry'
        db.create_table('common_timesheetentry', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Project'])),
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Task'])),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal('common', ['TimesheetEntry'])

        # Adding model 'TimesheetTimer'
        db.create_table('common_timesheettimer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Project'])),
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Task'])),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal('common', ['TimesheetTimer'])


    def backwards(self, orm):
        
        # Deleting model 'DebugControl'
        db.delete_table('common_debugcontrol')

        # Deleting model 'UserProfile'
        db.delete_table('common_userprofile')

        # Deleting model 'AuthenticationCode'
        db.delete_table('common_authenticationcode')

        # Deleting model 'SystemCounter'
        db.delete_table('common_systemcounter')

        # Deleting model 'Organization'
        db.delete_table('common_organization')

        # Deleting model 'OrganizationAccount'
        db.delete_table('common_organizationaccount')

        # Deleting model 'OrganizationCounter'
        db.delete_table('common_organizationcounter')

        # Deleting model 'UserMembership'
        db.delete_table('common_usermembership')

        # Deleting model 'UserPermissions'
        db.delete_table('common_userpermissions')

        # Deleting model 'Client'
        db.delete_table('common_client')

        # Deleting model 'SourceDocument'
        db.delete_table('common_sourcedocument')

        # Deleting model 'SourceDocumentMeta'
        db.delete_table('common_sourcedocumentmeta')

        # Deleting model 'SourceDocumentLine'
        db.delete_table('common_sourcedocumentline')

        # Deleting model 'SourceDocumentAllocation'
        db.delete_table('common_sourcedocumentallocation')

        # Deleting model 'Account'
        db.delete_table('common_account')

        # Deleting model 'AccountTransaction'
        db.delete_table('common_accounttransaction')

        # Deleting model 'AccountTransactionData'
        db.delete_table('common_accounttransactiondata')

        # Deleting model 'Activity'
        db.delete_table('common_activity')

        # Deleting model 'Task'
        db.delete_table('common_task')

        # Deleting model 'Project'
        db.delete_table('common_project')

        # Deleting model 'TimesheetEntry'
        db.delete_table('common_timesheetentry')

        # Deleting model 'TimesheetTimer'
        db.delete_table('common_timesheettimer')


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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Organization']"}),
            'refnum': ('django.db.models.fields.BigIntegerField', [], {}),
            'trading_name': ('django.db.models.fields.CharField', [], {'max_length': '192'})
        },
        'common.debugcontrol': {
            'Meta': {'object_name': 'DebugControl'},
            'current_time': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'common.organization': {
            'Meta': {'object_name': 'Organization'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'refnum': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True'}),
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
        'common.userpermissions': {
            'Meta': {'object_name': 'UserPermissions'},
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
