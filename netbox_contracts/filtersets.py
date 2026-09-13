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

    country = django_filters.ModelMultipleChoiceFilter(
        method='filter_country',
        queryset=Region.objects.all(),
        label='Country (Region)',
    )

    class Meta:
        model = Currency
        fields = (
            'id',
            'currency_code',
            'currency_name',
            'country',
            'currency_number',
            'usd_rate',
        )

    def filter_country(self, queryset, name, regions):
        if not regions:
            return queryset

        # Get the selected regions and all of their descendants
        region_ids = set()

        for region in regions:
            region_ids.add(region.pk)

            # NetBox Region uses a nested hierarchy
            descendants = region.get_descendants(include_self=False)
            region_ids.update(descendants.values_list('pk', flat=True))

        return queryset.filter(country_id__in=region_ids).distinct()

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset

        return queryset.filter(
            Q(currency_code__icontains=value) |
            Q(currency_name__icontains=value) |
            Q(currency_number__icontains=value)
        )