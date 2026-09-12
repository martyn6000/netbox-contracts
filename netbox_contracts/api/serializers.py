from netbox.api.serializers import NetBoxModelSerializer, WritableNestedSerializer
from rest_framework import serializers
from ..models import (
    Contract,
    ContractAssignment,
    ContractType,
    ServiceLevelAgreement,
    Currency,
)
from dcim.api.serializers import DeviceSerializer

class NestedContractSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_contracts-api:contract-detail'
    )
    yrc = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Contract
        fields = (
            'id',
            'url',
            'display',
            'name',
            'contract_type',
            'provider',
            'provider_account',
            'start_date',
            'end_date',
            'notice_period',
            'currency',
            'yrc',
            'nrc',
            'comments',
            'parent',
            'tags',
            'custom_fields',
            'created',
            'last_updated',
        )

class ContractTypeSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_contracts-api:contracttype-detail')

    class Meta:
        model = ContractType
        fields = (
            'id',
            'url',
            'display',
            'name',
            'description',
            'tags',
            'custom_fields',
            'created',
            'last_updated',
        )
        brief_fields = ('id', 'name', 'description', 'url', 'display')

class ContractSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_contracts-api:contract-detail'
    )
    contract_type = ContractTypeSerializer(nested=True, required=False, allow_null=True)
    yrc = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    parent = NestedContractSerializer(many=False, required=False)

    class Meta:
        model = Contract
        fields = (
            'id',
            'display',
            'name',
            'contract_type',
            'provider',
            'provider_account',
            'start_date',
            'end_date',
            'notice_period',
            'currency',
            'yrc',
            'nrc',
            'comments',
            'parent',
            'custom_fields',
            'tags',
            'created',
            'last_updated',
        )
        brief_fields = (
            'id',
            'url',
            'display',
            'name',
            'contract_type',
            'provider',
            'provider_account',
            'start_date',
            'end_date',
            'currency',
            'yrc',
            'nrc',
            'comments',
            'parent',
        )

class ContractAssignmentSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_contracts-api:contractassignment-detail'
    )
    class Meta:
        model = ContractAssignment
        fields = (
            'id',
            'display',
            'contract',
            'object_type',
            'object_id',
            'end_date',
            'yrc',
            'nrc',
            'sla',
            'fe',
            'fe_account',
            'custom_fields',
            'tags',
            'created',
            'last_updated',
        )

class ServiceLevelAgreementSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_contracts-api:servicelevelagreement-detail'
    )

    class Meta:
        model = ServiceLevelAgreement
        fields = (
            'id',
            'name',
            'description',
            'comments',
        )
        
class CurrencySerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_contracts-api:currency-detail'
    )

    class Meta:
        model = Currency
        fields = (
            'currency_code',
            'currency_number',
            'country',
            'currency_name',
        )