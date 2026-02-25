import django_filters
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from netbox.filtersets import NetBoxModelFilterSet, PrimaryModelFilterSet
from tenancy.filtersets import ContactModelFilterSet, TenancyFilterSet
from circuits.models import Provider, ProviderAccount
from dcim.models import Interface, Location, Region, Site, SiteGroup
from ipam.models import ASN
from .models import (
    AccountingDimension,
    AccountingDimensionStatusChoices,
    Contract,
    ContractAssignment,
    ContractType,
    CurrencyChoices,
    InternalEntityChoices,
    Invoice,
    InvoiceLine,
    ServiceProvider,
    StatusChoices,
    InvoiceStatusChoices,
)
from utilities.filters import (
    TreeNodeMultipleChoiceFilter,
)

class ContractFilterSet(ContactModelFilterSet, NetBoxModelFilterSet, TenancyFilterSet):
    status = django_filters.MultipleChoiceFilter(choices=StatusChoices, null_value=None)
    internal_party = django_filters.MultipleChoiceFilter(
        choices=InternalEntityChoices, null_value=None
    )
    currency = django_filters.MultipleChoiceFilter(
        choices=CurrencyChoices, null_value=None
    )
    contract_type = django_filters.ModelMultipleChoiceFilter(
        field_name='contract_type__name', to_field_name='name', queryset=ContractType.objects.all()
    )

    service_provider_id = django_filters.NumberFilter(
        field_name='external_party_object_id',
        method='filter_by_service_provider',
        label='Service provider'
    )

    provider_id = django_filters.NumberFilter(
        field_name='external_party_object_id',
        method='filter_by_circuit_provider',
        label='Circuit provider'
    )

    class Meta:
        model = Contract
        fields = (
            'id',
            'name',
            'status',
            'internal_party',
            'currency',
            'contract_type',
            'external_party_object_id',
            'external_reference',
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


class InvoiceFilterSet(NetBoxModelFilterSet):
    status = django_filters.MultipleChoiceFilter(choices=InvoiceStatusChoices, null_value=None)
    currency = django_filters.MultipleChoiceFilter(
        choices=CurrencyChoices, null_value=None
    )
    accounting_dimensions = django_filters.ModelChoiceFilter(
        field_name='invoicelines__accounting_dimensions',
        queryset=AccountingDimension.objects.all(),
        label='Accounting Dimension'
    )

    class Meta:
        model = Invoice
        fields = (
            'id',
            'number',
            'template',
            'date',
            'contracts',
            'period_start',
            'period_end',
            'amount',
        )

    def search(self, queryset, name, value):
        return queryset.filter(
            Q(number__icontains=value) | Q(contracts__name__icontains=value)
        )


class ServiceProviderFilterSet(ContactModelFilterSet, NetBoxModelFilterSet):
    class Meta:
        model = ServiceProvider
        fields = ('id', 'name')

    def search(self, queryset, name, value):
        return queryset.filter(name__icontains=value)


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


class InvoiceLineFilterSet(NetBoxModelFilterSet):
    currency = django_filters.MultipleChoiceFilter(
        choices=CurrencyChoices, null_value=None
    )

    class Meta:
        model = InvoiceLine
        fields = ('id', 'invoice', 'accounting_dimensions')

    def search(self, queryset, name, value):
        return queryset.filter(
            Q(comments__icontains=value) | Q(invoice__number__icontains=value)
        )


class AccountingDimensionFilterSet(NetBoxModelFilterSet):
    status = django_filters.MultipleChoiceFilter(
        choices=AccountingDimensionStatusChoices, null_value=None
    )

    class Meta:
        model = AccountingDimension
        fields = ('name', 'value')

    def search(self, queryset, name, value):
        return queryset.filter(Q(comments__icontains=value) | Q(name__icontains=value))

class ProviderFilterSet(PrimaryModelFilterSet, ContactModelFilterSet):
    region_id = TreeNodeMultipleChoiceFilter(
        queryset=Region.objects.all(),
        field_name='circuits__terminations___region',
        lookup_expr='in',
        label=_('Region (ID)'),
    )
    region = TreeNodeMultipleChoiceFilter(
        queryset=Region.objects.all(),
        field_name='circuits__terminations___region',
        lookup_expr='in',
        to_field_name='slug',
        label=_('Region (slug)'),
    )
    site_group_id = TreeNodeMultipleChoiceFilter(
        queryset=SiteGroup.objects.all(),
        field_name='circuits__terminations___site_group',
        lookup_expr='in',
        label=_('Site group (ID)'),
    )
    site_group = TreeNodeMultipleChoiceFilter(
        queryset=SiteGroup.objects.all(),
        field_name='circuits__terminations___site_group',
        lookup_expr='in',
        to_field_name='slug',
        label=_('Site group (slug)'),
    )
    site_id = django_filters.ModelMultipleChoiceFilter(
        field_name='circuits__terminations___site',
        queryset=Site.objects.all(),
        label=_('Site'),
    )
    site = django_filters.ModelMultipleChoiceFilter(
        field_name='circuits__terminations___site__slug',
        queryset=Site.objects.all(),
        to_field_name='slug',
        label=_('Site (slug)'),
    )
    asn_id = django_filters.ModelMultipleChoiceFilter(
        field_name='asns',
        queryset=ASN.objects.all(),
        label=_('ASN (ID)'),
    )
    asn = django_filters.ModelMultipleChoiceFilter(
        field_name='asns__asn',
        queryset=ASN.objects.all(),
        to_field_name='asn',
        label=_('ASN'),
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

class ProviderAccountFilterSet(PrimaryModelFilterSet, ContactModelFilterSet):
    provider_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Provider.objects.all(),
        distinct=False,
        label=_('Provider (ID)'),
    )
    provider = django_filters.ModelMultipleChoiceFilter(
        field_name='provider__slug',
        queryset=Provider.objects.all(),
        distinct=False,
        to_field_name='slug',
        label=_('Provider (slug)'),
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