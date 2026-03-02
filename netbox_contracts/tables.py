import django_tables2 as tables
from netbox.tables import NetBoxTable, columns
from tenancy.tables import ContactsColumnMixin

from .models import (
    Contract,
    ContractAssignment,
    ContractType,
    ServiceLevelAgreement,
)


class ContractTypeListTable(NetBoxTable):
    name = tables.Column(linkify=True)
    color = columns.ColorColumn()
    actions = columns.ActionsColumn(actions=('edit', 'delete'))

    class Meta(NetBoxTable.Meta):
        model = ContractType
        fields = ('pk', 'id', 'name', 'description', 'color', 'actions')
        default_columns = ('name', 'description', 'color')

class ContractAssignmentListTable(NetBoxTable):
    id = tables.Column(linkify=True)
    content_type = columns.ContentTypeColumn(verbose_name='Object Type')
    content_object = tables.Column(linkify=True, orderable=False)
    contract = tables.Column(linkify=True)
    actions = columns.ActionsColumn(actions=('edit', 'delete'))
    contract__external_party_object = tables.Column(linkify=True)
    tags = columns.TagColumn(url_name='plugins:netbox_contract:contractassignment_list')
    contract__contract_type = columns.ColoredLabelColumn(verbose_name='Contract type')

    class Meta(NetBoxTable.Meta):
        model = ContractAssignment
        fields = (
            'id',
            'content_type',
            'content_object',
            'contract',
            'contract__contract_type',
            'contract__external_party_object_type',
            'contract__external_party_object',
            'actions',
        )
        default_columns = (
            'id',
            'content_type',
            'content_object',
            'contract',
            'contract__contract_type',
            'contract__external_party_object_type',
            'contract__external_party_object',
        )

class ContractAssignmentObjectTable(NetBoxTable):
    contract = tables.Column(linkify=True)
    actions = columns.ActionsColumn(actions=('edit', 'delete'))
    contract__external_party_object = tables.Column(
        verbose_name='Partner', linkify=True
    )
    contract__status = columns.ChoiceFieldColumn(
        verbose_name=('Status'),
    )
    contract__contract_type = columns.ColoredLabelColumn(verbose_name='Contract type')
    contract_type = tables.Column(linkify=True, verbose_name='Contract type')

    class Meta(NetBoxTable.Meta):
        model = ContractAssignment
        fields = (
            'pk',
            'contract',
            'contract__external_party_object',
            'contract__status',
            'contract__contract_type',
            'contract__start_date',
            'contract__end_date',
            'contract__mrc',
            'contract__nrc',
            'actions',
        )
        default_columns = (
            'pk',
            'contract',
            'contract__external_party_object_type',
            'contract__external_party_object',
            'contract__status',
            'contract__contract_type',
            'contract__start_date',
            'contract__end_date',
            'contract__mrc',
            'contract__nrc',
        )

class ContractAssignmentContractTable(NetBoxTable):
    content_type = columns.ContentTypeColumn(verbose_name='Object Type')
    content_object = tables.Column(linkify=True, verbose_name='Object', orderable=False)
    content_object__status = columns.ChoiceFieldColumn(
        verbose_name=('Status'),
    )
    actions = columns.ActionsColumn(actions=('edit', 'delete'))

    class Meta(NetBoxTable.Meta):
        model = ContractAssignment
        fields = (
            'pk',
            'content_type',
            'content_object',
            'content_object__status',
            'actions',
        )
        default_columns = (
            'pk',
            'content_type',
            'content_object',
            'content_object__status',
        )

class ContractListTable(ContactsColumnMixin, NetBoxTable):
    name = tables.Column(linkify=True)
    external_party_object = tables.Column(verbose_name='External party', linkify=True)
    parent = tables.Column(linkify=True)
    yrc = tables.Column(verbose_name='Yerly recuring costs')
    status = columns.ChoiceFieldColumn(
        verbose_name=('Status'),
    )
    tags = columns.TagColumn(url_name='plugins:netbox_contract:contract_list')
    contract_type = tables.Column(linkify=True, verbose_name='Contract type')

    class Meta(NetBoxTable.Meta):
        model = Contract
        fields = (
            'pk',
            'id',
            'name',
            'contract_type',
            'external_party_object_type',
            'external_party_object',
            'external_reference',
            'internal_party',
            'tenant',
            'status',
            'start_date',
            'end_date',
            'initial_term',
            'renewal_term',
            'currency',
            'mrc',
            'yrc',
            'nrc',
            'invoice_frequency',
            'documents',
            'comments',
            'parent',
            'actions',
        )
        default_columns = ('name', 'status', 'contract_type', 'parent')

class ServiceLevelAgreementListTable(ContactsColumnMixin, NetBoxTable):
    name = tables.Column(linkify=True)
    description = tables.Column(linkify=True, verbose_name='Description')

    class Meta(NetBoxTable.Meta):
        model = ServiceLevelAgreement
        fields = (
            'pk',
            'id',
            'name',
            'actions',
        )
        default_columns = ('name', 'description')

class ContractListBottomTable(NetBoxTable):
    name = tables.Column(linkify=True)
    external_party_object = tables.Column(linkify=True)
    status = columns.ChoiceFieldColumn(
        verbose_name=('Status'),
    )

    class Meta(NetBoxTable.Meta):
        model = Contract
        fields = (
            'pk',
            'id',
            'name',
            'external_party_object_type',
            'external_party_object',
            'external_reference',
            'internal_party',
            'status',
            'mrc',
            'comments',
            'actions',
        )
        default_columns = (
            'name',
            'external_party_object_type',
            'external_party_object',
            'status',
        )

class ContractProviderBottomTable(NetBoxTable):
    name = tables.Column(linkify=True)
    external_party_object = tables.Column(linkify=True)
    status = columns.ChoiceFieldColumn(
        verbose_name=('Status'),
    )

    class Meta(NetBoxTable.Meta):
        model = Contract
        fields = (
            'pk',
            'id',
            'name',
            'start_date',
            'end_date',
            'external_reference',
            'status',
            'mrc',
            'comments',
            'actions',
        )
        default_columns = (
            'name',
            'status',
            'external_reference',
            'start_date',
            'end_date',
        )