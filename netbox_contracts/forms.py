from django import forms
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _
from netbox.forms import (
    NetBoxModelBulkEditForm,
    NetBoxModelFilterSetForm,
    NetBoxModelForm,
    NetBoxModelImportForm,
)
from circuits.models import Provider, ProviderAccount
from utilities.forms.fields import (
    ColorField,
    CommentField,
    ContentTypeChoiceField,
    CSVContentTypeField,
    CSVModelChoiceField,
    DynamicModelChoiceField,
    TagFilterField,
)
from utilities.forms.widgets import DatePicker, HTMXSelect
from .models import (
    Contract,
    ContractAssignment,
    ContractType,
    CurrencyChoices,
    ServiceLevelAgreement,
)
plugin_settings = settings.PLUGINS_CONFIG['netbox_contracts']

# Contract
class ContractForm(NetBoxModelForm):
    parent = DynamicModelChoiceField(
        queryset=Contract.objects.all(),
        required=False,
        selector=True,
        label=_('Parent'),
    )
    contract_type = DynamicModelChoiceField(
        queryset=ContractType.objects.all(), required=True, selector=True, label=_('Contract type')
    )

    provider = DynamicModelChoiceField(
        label=_('Provider'),
        queryset=Provider.objects.all(),
        selector=True,
        quick_add=True
    )
    
    provider_account = DynamicModelChoiceField(
        label=_('Provider account'),
        queryset=ProviderAccount.objects.all(),
        required=False,
        query_params={
            'provider_id': '$provider',
        }
    )
    comments = CommentField()

    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = Contract
        fields = (
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
            'parent',
            'documents',
            'comments',
            'tags',
        )

        widgets = {
            'start_date': DatePicker(),
            'end_date': DatePicker(),
        }

class ContractFilterForm(NetBoxModelFilterSetForm):
    model = Contract
    contract_type = DynamicModelChoiceField(
        queryset=ContractType.objects.all(),
        required=False,
        selector=True,
        label=_('Contract type'),
    )
    provider = DynamicModelChoiceField(
        queryset=Provider.objects.all(),
        required=False,
        selector=True,
        label=_('Provider'),
        help_text=_('Filter by Provider'),
    )
    provider_account = DynamicModelChoiceField(
        queryset=ProviderAccount.objects.all(),
        required=False,
        selector=True,
        label=_('Provider Account'),
        help_text=_('Filter by Provider Account'),
        query_params={
            'provider_id': '$provider',
        }
    )
    currency = forms.ChoiceField(
        choices=[('', '-----')] + list(CurrencyChoices),
        required=False,
        label=_('Currency')
    )
    parent = DynamicModelChoiceField(
        queryset=Contract.objects.all(),
        required=False,
        selector=True,
        label=_('Parent'),
    )
    tag = TagFilterField(model)

    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', None)
        super().__init__(*args, **kwargs)

class ContractCSVForm(NetBoxModelImportForm):
    parent = CSVModelChoiceField(
        queryset=Contract.objects.all(),
        to_field_name='name',
        help_text='Contract name',
        required=False,
        label=_('Parent'),
    )
    contract_type = CSVModelChoiceField(
        queryset=ContractType.objects.all(),
        to_field_name='name',
        help_text='Contract type name',
        required=False,
        label=_('Contract type'),
    )
    provider = CSVModelChoiceField(
        queryset=Provider.objects.all(),
        to_field_name='name',
        help_text='NetBox name of the provider ',
        required=True,
        label=_('Provider'),
    )
    provider_account = CSVModelChoiceField(
        queryset=ProviderAccount.objects.all(),
        to_field_name='account',
        help_text='NetBox account name of the provider account ',
        required=False,
        label=_('Provider Account'),
    )

    class Meta:
        model = Contract
        fields = [
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
            'documents',
            'parent',
        ]

class ContractBulkEditForm(NetBoxModelBulkEditForm):
    name = forms.CharField(max_length=100, required=False, label=_('Name'))
    contract_type = DynamicModelChoiceField(
        queryset=ContractType.objects.all(),
        required=False,
        selector=True,
        label=_('Contract Type')
    )
    comments = CommentField(required=False, label=_('Comments'))
    parent = DynamicModelChoiceField(
        queryset=Contract.objects.all(),
        required=False,
        selector=True,
        label=_('Parent'),
    )

    nullable_fields = ('comments',)
    model = Contract

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

# ContractType
class ContractTypeForm(NetBoxModelForm):
    color = ColorField(label=_('Color'))

    class Meta:
        model = ContractType
        fields = (
            'name',
            'description',
            'color',
            'tags',
        )

class ContractTypeCSVForm(NetBoxModelImportForm):
    name = forms.CharField(max_length=100, label=_('Name'))
    description = CommentField(label=_('Description'))
    color = ColorField(label=_('Color'))

    class Meta:
        model = ContractType
        fields = ['name', 'description', 'color']

class ContractTypeBulkEditForm(NetBoxModelBulkEditForm):
    description = CommentField(label=_('Description'))
    nullable_fields = ('comments',)
    color = ColorField(label=_('Color'), required=False,)
    model = ContractType

class ContractTypeFilterForm(NetBoxModelFilterSetForm):
    model = ContractType
    name = forms.CharField(required=False, label=_('Name'))
    description = CommentField(label=_('Description'))

# ContractAssignment
class ContractAssignmentForm(NetBoxModelForm):
    object_type = ContentTypeChoiceField(
        queryset=ContentType.objects.all(),
        widget=HTMXSelect(),
        label=_('Object Type'),
    )
    object = forms.ModelChoiceField(
        queryset=None, 
        label=_('Object')
    )
    fe = DynamicModelChoiceField(
        label=_('FE Vendor'),
        queryset=Provider.objects.all(),
        required=False,
    ) 
    fe_account = DynamicModelChoiceField(
        label=_('FE Vendor account'),
        queryset=ProviderAccount.objects.all(),
        required=False,
        query_params={
            'provider_id': '$fe',
        }
    )
    
    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', None)
        super().__init__(*args, **kwargs)

        # Initialize the object gfk
        if initial and 'object_type' in initial:
            object_type = ContentType.objects.get_for_id(initial['object_type'])
            object_class = object_type.model_class()
            self.fields['object'].queryset = object_class.objects.all()
            if (
                self.instance.object_type
                and self.instance.object_type.id == object_type.id
            ):
                self.fields['object'].initial = self.instance.object
            else:
                self.fields['object'].initial = None
        elif self.instance.object_type:
            object_class = self.instance.object_type.model_class()
            self.fields['object'].queryset = object_class.objects.all()
            self.fields['object'].initial = self.instance.object
        else:
            self.fields['object'].queryset = Provider.objects.all()
            self.fields['object'].initial = None

    class Meta:
        model = ContractAssignment
        fields = [
            'contract', 
            'end_date',
            'object_type',
            'object', 
            'yrc',
            'nrc',
            'sla',
            'fe',
            'fe_account',
            'tags'
        ]

        widgets = {
            'end_date': DatePicker(),
        }

class ContractAssignmentFilterForm(NetBoxModelFilterSetForm):
    model = ContractAssignment
    contract = DynamicModelChoiceField(
        queryset=Contract.objects.all(),
        required=False,
        selector=True,
        label=_('Contract'),
    )
    provider = DynamicModelChoiceField(
        queryset=Provider.objects.all(),
        required=False,
        selector=True,
        label=_('Provider'),
        help_text=_('Filter by Provider'),
    )
    provider_account = DynamicModelChoiceField(
        queryset=ProviderAccount.objects.all(),
        required=False,
        selector=True,
        label=_('Provider Account'),
        help_text=_('Filter by Provider Account'),
        query_params={
            'provider_id': '$provider',
        }
    )
    fe = DynamicModelChoiceField(
        queryset=Provider.objects.all(),
        required=False,
        selector=True,
        label=_('FE Vendor'),
        help_text=_('Filter by FE Vendor'),
    )
    fe_account = DynamicModelChoiceField(
        queryset=ProviderAccount.objects.all(),
        required=False,
        selector=True,
        label=_('FE Vendor Account'),
        help_text=_('Filter by FE Vendor Account'),
        query_params={
            'provider_id': '$fe',
        }
    )

class ContractAssignmentImportForm(NetBoxModelImportForm):
    object_type = CSVContentTypeField(
        queryset=ContentType.objects.all(),
        help_text='Content Type in the form <app>.<model>',
        label=_('Content type'),
    )
    contract = CSVModelChoiceField(
        queryset=Contract.objects.all(),
        help_text='ID of the contract to be imported',
        label=_('Contract'),
    )
    object_id = forms.CharField(
        required=True,
        help_text='ID of the object to be imported',
        label=_('Object ID')
    )
    class Meta:
        model = ContractAssignment
        fields = ['contract','object_type','object_id', 'tags']

class ContractAssignmentBulkEditForm(NetBoxModelBulkEditForm):
    contract = DynamicModelChoiceField(
        queryset=Contract.objects.all(),
        required=False,
        selector=True,
        label=_('Contract'),
    )
    model = ContractAssignment

# Service Level Agreement
class ServiceLevelAgreementForm(NetBoxModelForm):
    comments = CommentField()

    class Meta:
        model = ServiceLevelAgreement
        fields = ['name', 'description', 'comments', 'tags']

class ServiceLevelAgreementFilterForm(NetBoxModelFilterSetForm):
    model = ContractAssignment
    contract = DynamicModelChoiceField(
        queryset=ServiceLevelAgreement.objects.all(),
        required=False,
        selector=True,
        label=_('ServiceLevelAgreement'),
    )

class ServiceLevelAgreementImportForm(NetBoxModelImportForm):
    name = forms.CharField(required=False, label='SLA Name')
    description = forms.CharField(required=False, label='Description')
    model = ServiceLevelAgreement

    class Meta:
        model = ServiceLevelAgreement
        fields = ['name', 'description', 'tags']

class ServiceLevelAgreementBulkEditForm(NetBoxModelBulkEditForm):
    description = forms.CharField(required=False, label='Description')
    model = ServiceLevelAgreement