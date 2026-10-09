from dcim.api.serializers import ManufacturerSerializer
from django.contrib.contenttypes.models import ContentType
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from netbox.api.fields import ContentTypeField
from netbox.api.serializers import NetBoxModelSerializer, WritableNestedSerializer
from rest_framework import serializers
from utilities.api import get_serializer_for_model
from ..models import (
    Contract,
    ContractAssignment,
    ContractType,
    ServiceLevelAgreement,
    Currency,
    LicenseAssignment,
    LicenseType,
    SoftwareLicense,
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
            'comments',
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
    contract_status = serializers.CharField(read_only=True)
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
    currency = serializers.SlugRelatedField(
        slug_field='currency_code', 
        queryset=Currency.objects.all()
    )
    sla = NestedServiceLevelAgreementSerializer(read_only=True)
    assignment_status = serializers.CharField(read_only=True)

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


#
# Software licensing
#
class LicenseTypeSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_contracts-api:licensetype-detail'
    )

    class Meta:
        model = LicenseType
        fields = (
            'id',
            'url',
            'display',
            'name',
            'description',
            'color',
            'tags',
            'custom_fields',
            'created',
            'last_updated',
        )
        brief_fields = ('id', 'url', 'display', 'name', 'description', 'color')


class SoftwareLicenseSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_contracts-api:softwarelicense-detail'
    )
    manufacturer = ManufacturerSerializer(nested=True, required=True, allow_null=False)
    local_currency = CurrencySerializer(nested=True, required=False, allow_null=True)
    license_type = LicenseTypeSerializer(nested=True, required=False, allow_null=True)
    assignment_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = SoftwareLicense
        fields = (
            'id',
            'url',
            'display',
            'manufacturer',
            'license_name',
            'friendly_name',
            'license_sku',
            'per_license_cost',
            'local_currency',
            'license_type',
            'assignment_count',
            'tags',
            'custom_fields',
            'created',
            'last_updated',
        )
        brief_fields = ('id', 'url', 'display', 'license_name', 'friendly_name', 'license_sku')


class LicenseAssignmentSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_contracts-api:licenseassignment-detail'
    )
    software_license = SoftwareLicenseSerializer(nested=True)
    object_type = ContentTypeField(queryset=ContentType.objects.all())
    assigned_object = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = LicenseAssignment
        fields = (
            'id',
            'url',
            'display',
            'software_license',
            'object_type',
            'object_id',
            'assigned_object',
            'tags',
            'custom_fields',
            'created',
            'last_updated',
        )
        brief_fields = ('id', 'url', 'display')

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_assigned_object(self, instance):
        if instance.assigned_object is None:
            return None
        serializer = get_serializer_for_model(instance.assigned_object)
        context = {'request': self.context['request']}
        return serializer(instance.assigned_object, nested=True, context=context).data
