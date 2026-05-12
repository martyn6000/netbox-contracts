import django_tables2 as tables
from netbox.tables import NetBoxTable, columns, ChoiceFieldColumn
from circuits.models import Provider, ProviderAccount
from .models import (
    Contract,
    ContractAssignment,
    ContractType,
    ServiceLevelAgreement,
)
from django_tables2.utils import Accessor

class ProviderListTable(NetBoxTable):
    name = tables.Column(
        verbose_name=('Name'),
        linkify=True
    )
    accounts = columns.ManyToManyColumn(
        linkify_item=True,
        verbose_name=('Accounts')
    )
    account_count = columns.LinkedCountColumn(
        viewname='circuits:provideraccount_list',
        url_params={'provider_id': 'pk'},
        verbose_name=('Account Count')
    )
    asns = columns.ManyToManyColumn(
        linkify_item=True,
        verbose_name=('ASNs')
    )
    asn_count = columns.LinkedCountColumn(
        viewname='ipam:asn_list',
        url_params={'provider_id': 'pk'},
        verbose_name=('ASN Count')
    )
    circuit_count = columns.LinkedCountColumn(
        accessor=Accessor('count_circuits'),
        viewname='circuits:circuit_list',
        url_params={'provider_id': 'pk'},
        verbose_name=('Circuits')
    )
    tags = columns.TagColumn(
        url_name='circuits:provider_list'
    )

    class Meta(NetBoxTable.Meta):
        model = Provider
        fields = (
            'pk', 'id', 'name', 'accounts', 'account_count', 'asns', 'asn_count', 'circuit_count', 'description',
            'comments', 'contacts', 'tags', 'created', 'last_updated',
        )
        default_columns = ('pk', 'name', 'account_count', 'circuit_count')

class ProviderAccountListTable(NetBoxTable):
    account = tables.Column(
        linkify=True,
        verbose_name=('Account'),
    )
    name = tables.Column(
        verbose_name=('Name'),
    )
    provider = tables.Column(
        verbose_name=('Provider'),
        linkify=True
    )
    circuit_count = columns.LinkedCountColumn(
        accessor=Accessor('count_circuits'),
        viewname='circuits:circuit_list',
        url_params={'provider_account_id': 'pk'},
        verbose_name=('Circuits')
    )
    tags = columns.TagColumn(
        url_name='circuits:provideraccount_list'
    )

    class Meta(NetBoxTable.Meta):
        model = ProviderAccount
        fields = (
            'pk', 'id', 'account', 'name', 'provider', 'circuit_count', 'comments', 'contacts', 'tags', 'created',
            'last_updated',
        )
        default_columns = ('pk', 'account', 'name', 'provider', 'circuit_count')    

class ContractTypeListTable(NetBoxTable):
    name = tables.Column(linkify=True)
    color = columns.ColorColumn()
    actions = columns.ActionsColumn(actions=('edit', 'delete'))

    class Meta(NetBoxTable.Meta):
        model = ContractType
        fields = ('pk', 'id', 'name', 'description', 'color', 'comments', 'actions')
        default_columns = ('name', 'description', 'color')

class ContractAssignmentListTable(NetBoxTable):
    id = tables.Column(linkify=True)
    contract = tables.Column(linkify=True)
    object_type = columns.ContentTypeColumn(verbose_name='Object Type')
    object = tables.Column(linkify=True, orderable=False)
    actions = columns.ActionsColumn(actions=('edit', 'delete'))
    end_date = tables.Column(linkify=True)
    yrc = tables.Column(linkify=True)
    nrc = tables.Column(linkify=True)
    sla = tables.Column(linkify=True)
    fe = tables.Column(linkify=True)
    fe_account = tables.Column(linkify=True)
    tags = columns.TagColumn(url_name='plugins:netbox_contracts:contractassignment_list')
    contract__provider = tables.Column(linkify=True)
    contract__contract_type = columns.ColoredLabelColumn(verbose_name='Contract type')
    # object__region = tables.Column(linkify=True)
    assignment_status = ChoiceFieldColumn()
    device_serial = tables.Column(
        accessor='object.serial',
        verbose_name='Device Serial',
    )

    class Meta(NetBoxTable.Meta):
        model = ContractAssignment
        fields = (
            'contract',
            'object_type',
            'object',
            'end_date',
            'yrc',
            'nrc',
            'sla',
            'fe',
            'fe_account',
            'contract__provider',
            'contract__contract_type',
            'actions',
            'comments',
            'assignment_status',
            'device_serial',
        )
        default_columns = (
            'contract',
            'contract__contract_type',
            'contract__provider',
            'assignment_status',
            'object_type',
            'object',
            'device_serial',
            'end_date',
            'yrc',
            'nrc',
            'sla',
            'fe',
            'fe_account',
        )

class ContractAssignmentObjectTable(NetBoxTable):
    contract = tables.Column(linkify=True)
    actions = columns.ActionsColumn(actions=('edit', 'delete'))
    contract__provider = tables.Column(
        verbose_name='Provider', linkify=True
    )
    contract__provider_account = tables.Column(
        verbose_name='Provider account', linkify=True
    )
    fe = tables.Column(
        verbose_name='FE Provider', linkify=True
    )
    fe_account = tables.Column(
        verbose_name='FE Provider account', linkify=True
    )
    contract__contract_type = columns.ColoredLabelColumn(verbose_name='Contract type')
    assignment_status = ChoiceFieldColumn()

    class Meta(NetBoxTable.Meta):
        model = ContractAssignment
        fields = (
            'contract',
            'end_date',
            'yrc',
            'nrc',
            'sla',
            'fe',
            'fe_account',
            'contract__provider',
            'contract__provider_account',
            'contract__contract_type',
            'actions',
            'comments',
            'assignment_status',
        )
        default_columns = (
            'contract',
            'contract__contract_type',
            'contract__provider',
            'assignment_status',
            'end_date',
            'yrc',
            'nrc',
            'sla',
            'fe',
            'fe_account',
        )
        order_by = ('contract__status')

class ContractListTable(NetBoxTable):
    name = tables.Column(linkify=True)
    provider = tables.Column(linkify=True)
    parent = tables.Column(linkify=True)
    yrc = tables.Column(verbose_name='Yeerly recurring costs')
    tags = columns.TagColumn(url_name='plugins:netbox_contracts:contract_list')
    contract_type = tables.Column(linkify=True)
    provider_account = tables.Column(linkify=True) 
    start_date = tables.Column(linkify=True)
    end_date = tables.Column(linkify=True)
    term = tables.Column(linkify=True)
    notice_period = tables.Column(linkify=True)
    currency = tables.Column(linkify=True)
    yrc = tables.Column(linkify=True)
    nrc = tables.Column(linkify=True)
    documents = tables.Column(linkify=True)
    assgined_count = columns.LinkedCountColumn(
        viewname='plugins:netbox_contracts:contractassignment_list',
        url_params={'contract': 'pk'},
        verbose_name=('Assignments')
    )

    class Meta(NetBoxTable.Meta):
        model = Contract
        fields = (
            'pk',
            'name',
            'contract_type',
            'provider',
            'provider_account',
            'start_date',
            'end_date',
            'term',
            'notice_period'
            'currency',
            'yrc',
            'nrc',
            'documents',
            'parent',
            'comments',
            'assgined_count',
            'actions',
        )
        default_columns = (
            'pk',
            'name',
            'contract_type',
            'provider',
            'provider_account',
            'start_date',
            'end_date',
            'term',
            'notice_period'
            'currency',
            'yrc',
            'nrc',
            'documents',
            'assgined_count',
            'parent',
        )
        order_by = ('name')

class ServiceLevelAgreementListTable(NetBoxTable):
    name = tables.Column(linkify=True)
    description = tables.Column(linkify=True, verbose_name='Description')

    class Meta(NetBoxTable.Meta):
        model = ServiceLevelAgreement
        fields = (
            'pk',
            'id',
            'name',
            'description',
            'comments',
            'actions',
        )
        default_columns = ('name', 'description')
