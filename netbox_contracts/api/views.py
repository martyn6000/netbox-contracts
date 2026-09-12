from netbox.api.viewsets import NetBoxModelViewSet

from .. import filtersets, models
from .serializers import (
    ContractAssignmentSerializer,
    ContractSerializer,
    ContractTypeSerializer,
    ServiceLevelAgreementSerializer,
    CurrencySerializer,
)

class ContractViewSet(NetBoxModelViewSet):
    queryset = models.Contract.objects.prefetch_related(
        'contract_type',
        'provider',
        'provider_account',
        'currency_id',
        'parent',
        'tags',
        'custom_fields',
    )
    serializer_class = ContractSerializer
    filterset_class = filtersets.ContractFilterSet

class ContractAssignmentViewSet(NetBoxModelViewSet):
    queryset = models.ContractAssignment.objects.prefetch_related(
        'contract',
        'object_type',
        'currency_id',
        'sla',
        'provider',
        'provider_account',
        'fe',
        'fe_account',
        'tags',
        'custom_fields',
    )
    serializer_class = ContractAssignmentSerializer

class ContractTypeViewSet(NetBoxModelViewSet):
    queryset = models.ContractType.objects.prefetch_related(
        'tags',
        'custom_fields',
    )
    serializer_class = ContractTypeSerializer

class ServiceLevelAgreementViewSet(NetBoxModelViewSet):
    queryset = models.ServiceLevelAgreement.objects.prefetch_related(
        'tags',
        'custom_fields',
    )
    serializer_class = ServiceLevelAgreementSerializer

class CurrencyViewSet(NetBoxModelViewSet):
    queryset = models.Currency.objects.prefetch_related(
        'country',
        'tags',
        'custom_fields',
    )
    serializer_class = CurrencySerializer

