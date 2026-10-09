from netbox.api.viewsets import NetBoxModelViewSet

from .. import filtersets, models
from .serializers import (
    ContractAssignmentSerializer,
    ContractSerializer,
    ContractTypeSerializer,
    ServiceLevelAgreementSerializer,
    CurrencySerializer,
    LicenseAssignmentSerializer,
    LicenseTypeSerializer,
    SoftwareLicenseSerializer,
)

class ContractViewSet(NetBoxModelViewSet):
    queryset = models.Contract.objects.select_related(
        'contract_type',
        'provider',
        'provider_account',
        'currency',
        'parent',
    ).prefetch_related(
        'tags',
    )
    serializer_class = ContractSerializer
    filterset_class = filtersets.ContractFilterSet

class ContractAssignmentViewSet(NetBoxModelViewSet):
    queryset = models.ContractAssignment.objects.select_related(
        'contract',
        'object_type',
        'currency',
        'sla',
        'provider',
        'provider_account',
        'fe',
        'fe_account',
    ).prefetch_related(
        'tags',
    )
    serializer_class = ContractAssignmentSerializer

class ContractTypeViewSet(NetBoxModelViewSet):
    queryset = models.ContractType.objects.prefetch_related(
        'tags',
    )
    serializer_class = ContractTypeSerializer

class ServiceLevelAgreementViewSet(NetBoxModelViewSet):
    queryset = models.ServiceLevelAgreement.objects.prefetch_related(
        'tags',
    )
    serializer_class = ServiceLevelAgreementSerializer

class CurrencyViewSet(NetBoxModelViewSet):
    queryset = models.Currency.objects.select_related(
        'country',
    ).prefetch_related(
        'tags',
    )
    serializer_class = CurrencySerializer

class LicenseTypeViewSet(NetBoxModelViewSet):
    queryset = models.LicenseType.objects.prefetch_related(
        'tags',
    )
    serializer_class = LicenseTypeSerializer
    filterset_class = filtersets.LicenseTypeFilterSet

class SoftwareLicenseViewSet(NetBoxModelViewSet):
    queryset = models.SoftwareLicense.objects.select_related(
        'manufacturer',
        'local_currency',
        'license_type',
    ).prefetch_related(
        'tags',
    )
    serializer_class = SoftwareLicenseSerializer
    filterset_class = filtersets.SoftwareLicenseFilterSet

class LicenseAssignmentViewSet(NetBoxModelViewSet):
    queryset = models.LicenseAssignment.objects.select_related(
        'software_license',
        'object_type',
    ).prefetch_related(
        'tags',
    )
    serializer_class = LicenseAssignmentSerializer
    filterset_class = filtersets.LicenseAssignmentFilterSet
