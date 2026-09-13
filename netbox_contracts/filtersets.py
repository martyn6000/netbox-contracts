import django_filters
from django.db.models import Q
from netbox.filtersets import NetBoxModelFilterSet
from django_filters import ModelChoiceFilter, ModelMultipleChoiceFilter
from dcim.models import Region

from .models import (
    Contract,
    ContractAssignment,
    ContractType,
    Currency,
    ServiceLevelAgreement,
)
__all__ = (
    'ContractFilterSet',
    'ContractTypeFilterSet',
    'ServiceLevelAgreementFilterSet',
    'ContractAssignmentFilterSet',
    'CurrencyFilterSet',
)

class ContractFilterSet(NetBoxModelFilterSet):
    # currency = django_filters.MultipleChoiceFilter(
    #     choices=CurrencyChoices, null_value=None
    # )
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

    def search(self, queryset, name, value):
        return queryset.filter(name__icontains=value)

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

class CurrencyFilterSet(NetBoxModelFilterSet):
    country = ModelMultipleChoiceFilter(
        field_name='country__slug', # Traverses to the slug or name
        to_field_name='slug',
        queryset=Region.objects.all(),
        label='Country (Region)',
    )

    currency_code = django_filters.ModelMultipleChoiceFilter(
        field_name='currency_code',
        to_field_name='currency_code',
        queryset=Currency.objects.all(),
        label='Currency Code',
    )
    currency_name = django_filters.ModelMultipleChoiceFilter(
        field_name='currency_name',
        to_field_name='currency_name',
        queryset=Currency.objects.all(),
        label='Currency Name',
    )

    class Meta:
        model = Currency
        fields = ('id', 'currency_code','currency_name', 'country', 'currency_number', 'usd_rate')

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        
        # Define which fields the quick search box actually looks at
        return queryset.filter(
            Q(currency_code__icontains=value) | 
            Q(currency_name__icontains=value) | 
            Q(currency_number__icontains=value)
        )