import django_filters
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from circuits.models import Circuit, CircuitTermination
from dcim.models import Device, Region, Site
from netbox.filtersets import NetBoxModelFilterSet
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

    contract_type = django_filters.ModelMultipleChoiceFilter(
        field_name='contract_type__name',
        to_field_name='name',
        queryset=ContractType.objects.all(),
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
        if not value.strip():
            return queryset

        return queryset.filter(name__icontains=value)


class ContractTypeFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = ContractType
        fields = (
            'name',
            'description',
            'color',
        )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset

        return queryset.filter(name__icontains=value)


class ServiceLevelAgreementFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = ServiceLevelAgreement
        fields = (
            'name',
            'description',
        )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset

        return queryset.filter(name__icontains=value)


class ContractAssignmentFilterSet(NetBoxModelFilterSet):

    region = django_filters.ModelMultipleChoiceFilter(
        method='filter_region',
        queryset=Region.objects.all(),
        label='Region',
    )

    class Meta:
        model = ContractAssignment
        fields = (
            'id',
            'contract',
            'provider',
            'fe',
            'object_type',
            'object_id',
            'region',
        )

    def filter_region(self, queryset, name, regions):
        if not regions:
            return queryset

        region_ids = set()

        # Include selected regions and all descendant regions.
        for region in regions:
            region_ids.add(region.pk)
            region_ids.update(
                region.get_descendants(include_self=False)
                .values_list('pk', flat=True)
            )

        #
        # Sites in the selected region hierarchy
        #
        site_ids = Site.objects.filter(
            region_id__in=region_ids
        ).values_list('pk', flat=True)

        #
        # Devices located at matching sites
        #
        device_ids = Device.objects.filter(
            site_id__in=site_ids
        ).values_list('pk', flat=True)

        #
        # NetBox 4.3.1:
        #
        # CircuitTermination.termination is a GenericForeignKey backed by:
        #
        #   termination_type
        #   termination_id
        #
        # Only circuits whose A-side terminates directly at a Site are
        # included here.
        #
        site_content_type = ContentType.objects.get_for_model(
            Site,
            for_concrete_model=False,
        )

        circuit_ids = CircuitTermination.objects.filter(
            term_side='A',
            termination_type_id=site_content_type.pk,
            termination_id__in=site_ids,
        ).values_list('circuit_id', flat=True)

        #
        # Content types used by ContractAssignment.object_type
        #
        device_content_type = ContentType.objects.get_for_model(
            Device,
            for_concrete_model=False,
        )

        circuit_content_type = ContentType.objects.get_for_model(
            Circuit,
            for_concrete_model=False,
        )

        #
        # object_id must always be evaluated together with object_type,
        # because Device and Circuit primary keys can overlap.
        #
        return queryset.filter(
            Q(
                object_type_id=device_content_type.pk,
                object_id__in=device_ids,
            )
            |
            Q(
                object_type_id=circuit_content_type.pk,
                object_id__in=circuit_ids,
            )
        ).distinct()

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset

        return queryset.filter(
            Q(contract__name__icontains=value)
        )


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

        region_ids = set()

        # Include selected regions and all descendant regions.
        for region in regions:
            region_ids.add(region.pk)
            region_ids.update(
                region.get_descendants(include_self=False)
                .values_list('pk', flat=True)
            )

        return queryset.filter(
            country_id__in=region_ids
        ).distinct()

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset

        return queryset.filter(
            Q(currency_code__icontains=value)
            | Q(currency_name__icontains=value)
            | Q(currency_number__icontains=value)
        )
