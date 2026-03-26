from django.contrib.auth.models import ContentType
from drf_yasg.utils import swagger_serializer_method
from netbox.api.fields import ContentTypeField
from netbox.api.serializers import NetBoxModelSerializer, WritableNestedSerializer
from rest_framework import serializers
from utilities.api import get_serializer_for_model
from ..models import (
    Contract,
    ContractAssignment,
    ContractType,
    ServiceLevelAgreement,
)

class NestedContractSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_contracts-api:contract-detail'
    )
    yrc = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Contract
        fields = fields = (
            'id',
            'url',
            'display',
            'name',
            'contract_type',
            'status',
            'start_date',
            'end_date',
            'currency',
            'yrc',
            'nrc',
            'comments',
        )

    @swagger_serializer_method(serializer_or_field=serializers.JSONField)
    def get_external_party_object(self, instance):
        serializer = get_serializer_for_model(
            instance.external_party_object_type.model_class()
        )
        context = {'request': self.context['request']}
        return serializer(
            instance.external_party_object, nested=True, context=context
        ).data

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
            'url',
            'display',
            'name',
            'contract_type',
            'status',
            'start_date',
            'end_date',
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
        brief_fields = (
            'id',
            'url',
            'display',
            'name',
            'contract_type',
            'status',
            'start_date',
            'end_date',
            'currency',
            'yrc',
            'nrc',
            'comments',
            'parent',
        )

    @swagger_serializer_method(serializer_or_field=serializers.JSONField)
    def get_external_party_object(self, instance):
        serializer = get_serializer_for_model(
            instance.external_party_object_type.model_class()
        )
        context = {'request': self.context['request']}
        return serializer(
            instance.external_party_object, nested=True, context=context
        ).data

class ContractAssignmentSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_contracts-api:contractassignment-detail'
    )
    object_type = ContentTypeField(queryset=ContentType.objects.all())
    object = serializers.SerializerMethodField(read_only=True)
    contract = NestedContractSerializer()

    class Meta:
        model = ContractAssignment
        fields = (
            'id',
            'url',
            'display',
            'object_type',
            'object',
            'contract',
            'created',
            'last_updated',
        )
        brief_fields = ('id', 'url', 'display', 'object', 'contract')

    @swagger_serializer_method(serializer_or_field=serializers.JSONField)
    def get_object(self, instance):
        serializer = get_serializer_for_model(instance.object_type.model_class())
        context = {'request': self.context['request']}
        return serializer(instance.object, nested=True, context=context).data
    
class ServiceLevelAgreementSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_contracts-api:servicelevelagreement-detail'
    )

    class Meta:
        model = ServiceLevelAgreement
        fields = (
            'pk',
            'id',
            'name',
            'description',
            'comments',
        )