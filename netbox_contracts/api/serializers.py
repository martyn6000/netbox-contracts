from netbox.api.serializers import NetBoxModelSerializer, WritableNestedSerializer
from rest_framework import serializers
from ..models import (
    Contract,
    ContractAssignment,
    ContractType,
    ServiceLevelAgreement,
    Currency,
)

class NestedContractTypeSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_contracts-api:contracttype-detail'
    )

    class Meta:
        model = ContractType
        fields = ('id', 'url', 'display', 'name')

class NestedContractSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_contracts-api:contract-detail'
    )

    class Meta:
        model = Contract
        fields = ('id', 'url', 'display', 'name')

class NestedCurrencySerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_contracts-api:currency-detail'
    )

    class Meta:
        model = Currency
        fields = ('id', 'url', 'display', 'currency_code')

class NestedServiceLevelAgreementSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_contracts-api:servicelevelagreement-detail'
    )

    class Meta:
        model = ServiceLevelAgreement
        fields = ('id', 'url', 'display', 'name')

class ContractTypeSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_contracts-api:contracttype-detail'
    )

    class Meta:
        model = ContractType
        fields = (
            'id',
            'url',
            'display',
            'name',
            'description',
            'color',
            'comments',
            'tags',
            'custom_fields',
            'created',
            'last_updated',
        )
        brief_fields = ('id', 'url', 'display', 'name', 'color')

class CurrencySerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_contracts-api:currency-detail'
    )

    class Meta:
        model = Currency
        fields = (
            'id',
            'url',
            'display',
            'currency_code',
            'currency_name',
            'currency_number',
            'country',
            'usd_rate',
            'tags',
            'custom_fields',
            'created',
            'last_updated',
        )
        brief_fields = ('id', 'url', 'display', 'currency_code', 'currency_name')

class ServiceLevelAgreementSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_contracts-api:servicelevelagreement-detail'
    )

    class Meta:
        model = ServiceLevelAgreement
        fields = (
            'id',
            'url',
            'display',
            'name',
            'description',
            'comments',
            'tags',
            'custom_fields',
            'created',
            'last_updated',
        )
        brief_fields = ('id', 'url', 'display', 'name')

class ContractSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_contracts-api:contract-detail'
    )
    contract_type = NestedContractTypeSerializer(read_only=True)
    currency = NestedCurrencySerializer(read_only=True)
    parent = NestedContractSerializer(read_only=True)
    contract_status = serializers.CharField(read_only=True, source='contract_status')
    contract_length = serializers.SerializerMethodField()
    notice_date = serializers.SerializerMethodField()
    yrc_usd = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True, allow_null=True)
    nrc_usd = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True, allow_null=True)

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
            'notice_date',
            'contract_length',
            'contract_status',
            'currency',
            'yrc',
            'nrc',
            'yrc_usd',
            'nrc_usd',
            'documents',
            'comments',
            'parent',
            'tags',
            'custom_fields',
            'created',
            'last_updated',
        )
        brief_fields = (
            'id',
            'url',
            'display',
            'name',
            'contract_type',
            'start_date',
            'end_date',
            'contract_status',
        )

    def get_contract_length(self, obj):
        return obj.contract_length()

    def get_notice_date(self, obj):
        if obj.end_date and obj.notice_period:
            return obj.notice_date()
        return None

class ContractAssignmentSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_contracts-api:contractassignment-detail'
    )
    contract = NestedContractSerializer(read_only=True)
    currency = NestedCurrencySerializer(read_only=True)
    sla = NestedServiceLevelAgreementSerializer(read_only=True)
    assignment_status = serializers.CharField(read_only=True, source='assignment_status')

    class Meta:
        model = ContractAssignment
        fields = (
            'id',
            'url',
            'display',
            'contract',
            'object_type',
            'object_id',
            'end_date',
            'currency',
            'yrc',
            'nrc',
            'sla',
            'provider',
            'provider_account',
            'fe',  # Field Engineer provider
            'fe_account',  # Field Engineer account
            'assignment_status',
            'comments',
            'tags',
            'custom_fields',
            'created',
            'last_updated',
        )
        brief_fields = (
            'id',
            'url',
            'display',
            'contract',
            'assignment_status',
        )