import django_filters
from django.db.models import Q
from netbox.filtersets import NetBoxModelFilterSet

from .models import (
    Contract,
    ContractAssignment,
    ContractType,
    CurrencyChoices,
    ServiceLevelAgreement,
)
__all__ = (
    'NestedGroupModelFilterSetForm',
    'NetBoxModelFilterSetForm',
    'OrganizationalModelFilterSetForm',
    'ProviderAccountFilterSet',
    'ProviderFilterSet',
)

class ContractFilterSet(NetBoxModelFilterSet):
    currency = django_filters.MultipleChoiceFilter(
        choices=CurrencyChoices, null_value=None
    )
    contract_type = django_filters.ModelMultipleChoiceFilter(
        field_name='contract_type__name', to_field_name='name', queryset=ContractType.objects.all()
    )

    class Meta:
        model = Contract
        fields = (
            'id',
            'name',
            'currency',
            'contract_type',
            'parent',
        )

class ContractTypeFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = ContractType
        fields = ('name', 'description', 'color')

    def search(self, queryset, name, value):
        return queryset.filter(name__icontains=value)

class ServiceLevelAgreementFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = ServiceLevelAgreement
        fields = ('name', 'description')

    def search(self, queryset, name, value):
        return queryset.filter(name__icontains=value)

class ContractAssignmentFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = ContractAssignment
        fields = ('id', 'contract', 'provider', 'fe', 'object_id')

    def search(self, queryset, name, value):
        return queryset.filter(Q(contract__name__icontains=value))