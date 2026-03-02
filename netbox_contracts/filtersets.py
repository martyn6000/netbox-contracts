import django_filters
from django import forms
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from netbox.filtersets import NetBoxModelFilterSet, PrimaryModelFilterSet
from tenancy.filtersets import ContactModelFilterSet, TenancyFilterSet
from circuits.models import Provider, ProviderAccount
from dcim.models import Interface, Location, Region, Site, SiteGroup
from ipam.models import ASN
from .models import (
    Contract,
    ContractAssignment,
    ContractType,
    CurrencyChoices,
    InternalEntityChoices,
    StatusChoices,
    ServiceLevelAgreement,
)
from utilities.filters import (
    TreeNodeMultipleChoiceFilter,
)
from utilities.filtersets import register_filterset

__all__ = (
    'NestedGroupModelFilterSetForm',
    'NetBoxModelFilterSetForm',
    'OrganizationalModelFilterSetForm',
    'PrimaryModelFilterSetForm',
    'ProviderAccountFilterSet',
    'ProviderFilterSet',
)

class ContractFilterSet(ContactModelFilterSet, NetBoxModelFilterSet):
    status = django_filters.MultipleChoiceFilter(choices=StatusChoices, null_value=None)
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
            'status',
            'currency',
            'contract_type',
            'parent',
        )

    def search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value)
            | Q(external_reference__icontains=value)
            | Q(comments__icontains=value),
            Q(status__iexact='Active'),
        )

    def filter_by_service_provider(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(
            external_party_object_id=value,
            external_party_object_type=ContentType.objects.get_for_model(ServiceProvider)
        )

    def filter_by_circuit_provider(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(
            external_party_object_id=value,
            external_party_object_type=ContentType.objects.get_for_model(Provider)
        )

class ContractTypeFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = ContractType
        fields = ('name', 'description', 'color')

    def search(self, queryset, name, value):
        return queryset.filter(name__icontains=value)

class ContractAssignmentFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = ContractAssignment
        fields = ('id', 'contract')

    def search(self, queryset, name, value):
        return queryset.filter(Q(contract__name__icontains=value))

@register_filterset
class ProviderFilterSet(PrimaryModelFilterSet, ContactModelFilterSet):
    region_id = TreeNodeMultipleChoiceFilter(
        queryset=Region.objects.all(),
        field_name='circuits__terminations___region',
        lookup_expr='in',
        label=('Region (ID)'),
    )
    region = TreeNodeMultipleChoiceFilter(
        queryset=Region.objects.all(),
        field_name='circuits__terminations___region',
        lookup_expr='in',
        to_field_name='slug',
        label=('Region (slug)'),
    )
    site_group_id = TreeNodeMultipleChoiceFilter(
        queryset=SiteGroup.objects.all(),
        field_name='circuits__terminations___site_group',
        lookup_expr='in',
        label=('Site group (ID)'),
    )
    site_group = TreeNodeMultipleChoiceFilter(
        queryset=SiteGroup.objects.all(),
        field_name='circuits__terminations___site_group',
        lookup_expr='in',
        to_field_name='slug',
        label=('Site group (slug)'),
    )
    site_id = django_filters.ModelMultipleChoiceFilter(
        field_name='circuits__terminations___site',
        queryset=Site.objects.all(),
        label=('Site'),
    )
    site = django_filters.ModelMultipleChoiceFilter(
        field_name='circuits__terminations___site__slug',
        queryset=Site.objects.all(),
        to_field_name='slug',
        label=('Site (slug)'),
    )
    asn_id = django_filters.ModelMultipleChoiceFilter(
        field_name='asns',
        queryset=ASN.objects.all(),
        label=('ASN (ID)'),
    )
    asn = django_filters.ModelMultipleChoiceFilter(
        field_name='asns__asn',
        queryset=ASN.objects.all(),
        to_field_name='asn',
        label=('ASN'),
    )

    class Meta:
        model = Provider
        fields = ('id', 'name', 'slug', 'description')

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value) |
            Q(description__icontains=value) |
            Q(comments__icontains=value)
        )
    
@register_filterset
class ProviderAccountFilterSet(PrimaryModelFilterSet, ContactModelFilterSet):
    provider_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Provider.objects.all(),
        distinct=False,
        label=('Provider (ID)'),
    )
    provider = django_filters.ModelMultipleChoiceFilter(
        field_name='provider__slug',
        queryset=Provider.objects.all(),
        distinct=False,
        to_field_name='slug',
        label=('Provider (slug)'),
    )

    class Meta:
        model = ProviderAccount
        fields = ('id', 'name', 'account', 'description')

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value) |
            Q(description__icontains=value) |
            Q(account__icontains=value) |
            Q(comments__icontains=value)
        ).distinct()

class ServiceLevelAgreementFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = ServiceLevelAgreement
        fields = ('name', 'description')

    def search(self, queryset, name, value):
        return queryset.filter(name__icontains=value)