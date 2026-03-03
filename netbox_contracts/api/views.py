from django.db.models import Case, F, When
from django.db.models.functions import Round
from netbox.api.viewsets import NetBoxModelViewSet

from .. import filtersets, models
from .serializers import (
    ContractAssignmentSerializer,
    ContractSerializer,
    ContractTypeSerializer,
)

class ContractViewSet(NetBoxModelViewSet):
    queryset = models.Contract.objects.prefetch_related('parent', 'tags')
    serializer_class = ContractSerializer
    filterset_class = filtersets.ContractFilterSet

class ContractAssignmentViewSet(NetBoxModelViewSet):
    queryset = models.ContractAssignment.objects.prefetch_related('contract', 'tags')
    serializer_class = ContractAssignmentSerializer

class ContractTypeViewSet(NetBoxModelViewSet):
    queryset = models.ContractType.objects.prefetch_related('tags')
    serializer_class = ContractTypeSerializer
