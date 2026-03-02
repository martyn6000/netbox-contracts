from django import forms
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.utils.translation import gettext_lazy as _
from netbox.forms import (
    NetBoxModelBulkEditForm,
    NetBoxModelFilterSetForm,
    NetBoxModelForm,
    NetBoxModelImportForm,
    PrimaryModelForm,
)
from tenancy.forms import ContactModelFilterForm, TenancyFilterForm
from tenancy.models import Tenant
from circuits.models import Provider, ProviderAccount
from utilities.forms import BOOLEAN_WITH_BLANK_CHOICES, get_field_value
from utilities.forms.fields import (
    ColorField,
    CommentField,
    ContentTypeChoiceField,
    CSVChoiceField,
    CSVContentTypeField,
    CSVModelChoiceField,
    DynamicModelChoiceField,
    DynamicModelMultipleChoiceField,
    SlugField,
    TagFilterField,
)
from utilities.forms.rendering import FieldSet, InlineFields
from utilities.forms.widgets import DatePicker, HTMXSelect
from utilities.templatetags.builtins.filters import bettertitle

from .constants import ASSIGNEMENT_MODELS, SERVICE_PROVIDER_MODELS, SERVICE_PROVIDER_TYPES
from .models import (
    Contract,
    ContractAssignment,
    ContractType,
    CurrencyChoices,
    InternalEntityChoices,
    ServiceLevelAgreement,
    StatusChoices,
)
from ipam.models import ASN
from netbox.forms.mixins import OwnerMixin

plugin_settings = settings.PLUGINS_CONFIG['netbox_contracts']

class PrimaryModelBulkEditForm(OwnerMixin, NetBoxModelBulkEditForm):
    """
    Bulk edit form for models which inherit from PrimaryModel.
    """
    description = forms.CharField(
        label=_('Description'),
        max_length=100,
        required=False
    )
    comments = CommentField()

# Contract
class ContractForm(NetBoxModelForm):
    comments = CommentField(label=_('Comments'))

    external_party_object_type = ContentTypeChoiceField(
        queryset=ContentType.objects.all(),
        limit_choices_to=SERVICE_PROVIDER_MODELS,
        widget=HTMXSelect(),
        label=_('External party object type'),
    )
    external_party_object = forms.ModelChoiceField(queryset=None, label=_('External party object'))
    tenant = DynamicModelChoiceField(queryset=Tenant.objects.all(), required=False, selector=True, label=_('Tenant'))
    parent = DynamicModelChoiceField(
        queryset=Contract.objects.all(),
        required=False,
        selector=True,
        label=_('Parent'),
    )
    contract_type = DynamicModelChoiceField(
        queryset=ContractType.objects.all(), required=False, selector=True, label=_('Contract type')
    )

    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', None)
        super().__init__(*args, **kwargs)

        # Initialise fields settings
        mandatory_fields = plugin_settings.get('mandatory_contract_fields')
        for field in mandatory_fields:
            self.fields[field].required = True
        hidden_fields = plugin_settings.get('hidden_contract_fields')
        for field in hidden_fields:
            if not self.fields[field].required:
                self.fields[field].widget = forms.HiddenInput()

    class Meta:
        model = Contract
        fields = (
            'name',
            'contract_type',
            'tenant',
            'status',
            'start_date',
            'end_date',
            'notice_period',
            'currency',
            'mrc',
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

    def clean(self):
        super().clean()

        if self.cleaned_data['mrc'] and self.cleaned_data['yrc']:
            raise ValidationError('you should set monthly OR yearly recuring costs not both')


class ContractFilterForm(ContactModelFilterForm, TenancyFilterForm, NetBoxModelFilterSetForm):
    model = Contract

    contract_type = DynamicModelChoiceField(
        queryset=ContractType.objects.all(),
        required=False,
        selector=True,
        label=_('Contract type'),
    )

    provider_id = DynamicModelChoiceField(
        queryset=Provider.objects.all(),
        required=False,
        selector=True,
        label=_('Circuit Provider'),
        help_text=_('Filter by Circuit Provider'),
    )

    external_reference = forms.CharField(required=False, label=_('External reference'))

    internal_party = forms.ChoiceField(
        choices=[('', '-----')] + list(InternalEntityChoices),
        required=False,
        label=_('Internal party')
    )

    status = forms.ChoiceField(choices=StatusChoices, required=False, label=_('Status'))

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


class ContractCSVForm(NetBoxModelImportForm):
    tenant = CSVModelChoiceField(
        queryset=Tenant.objects.all(),
        to_field_name='name',
        help_text='Tenant name',
        required=False,
        label=_('Tenant'),
    )
    status = CSVChoiceField(choices=StatusChoices, help_text='Contract status', label=_('Status'))
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

    class Meta:
        model = Contract
        fields = [
            'name',
            'contract_type',
            'tenant',
            'status',
            'start_date',
            'end_date',
            'currency',
            'mrc',
            'nrc',
            'documents',
            'comments',
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

    external_reference = forms.CharField(max_length=100, required=False, label=_('External reference'))
    internal_party = forms.ChoiceField(choices=InternalEntityChoices, required=False, label=_('Internal party'))
    tenant = DynamicModelChoiceField(queryset=Tenant.objects.all(), required=False, selector=True, label=_('Tenant'))
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

        if external_party_object_type_id := get_field_value(self, 'external_party_object_type'):
            try:
                external_party_object_type = ContentType.objects.get(pk=external_party_object_type_id)
                model = external_party_object_type.model_class()
                self.fields['external_party_object'].queryset = model.objects.all()
                self.fields['external_party_object'].widget.attrs['selector'] = model._meta.label_lower
                self.fields['external_party_object'].disabled = False
                self.fields['external_party_object'].label = _(bettertitle(model._meta.verbose_name))
            except ObjectDoesNotExist:
                pass

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

# Circuit Provider forms
class ProviderForm(PrimaryModelForm):
    slug = SlugField()
    asns = DynamicModelMultipleChoiceField(
        queryset=ASN.objects.all(),
        label=_('ASNs'),
        required=False
    )

    fieldsets = (
        FieldSet('name', 'slug', 'asns', 'description', 'tags'),
    )

    class Meta:
        model = Provider
        fields = [
            'name', 'slug', 'asns', 'description', 'owner', 'comments', 'tags',
        ]

class ProviderAccountForm(PrimaryModelForm):
    provider = DynamicModelChoiceField(
        label=_('Provider'),
        queryset=Provider.objects.all(),
        selector=True,
        quick_add=True
    )

    class Meta:
        model = ProviderAccount
        fields = [
            'provider', 'name', 'account', 'description', 'owner', 'comments', 'tags',
        ]

class ProviderBulkEditForm(PrimaryModelBulkEditForm):
    asns = DynamicModelMultipleChoiceField(
        queryset=ASN.objects.all(),
        label=_('ASNs'),
        required=False
    )

    model = Provider
    fieldsets = (
        FieldSet('asns', 'description'),
    )
    nullable_fields = (
        'asns', 'description', 'comments',
    )

class ProviderAccountBulkEditForm(PrimaryModelBulkEditForm):
    provider = DynamicModelChoiceField(
        label=_('Provider'),
        queryset=Provider.objects.all(),
        required=False
    )

    model = ProviderAccount
    fieldsets = (
        FieldSet('provider', 'description'),
    )
    nullable_fields = (
        'description', 'comments',
    )

# ContractAssignment
class ContractAssignmentForm(NetBoxModelForm):

    content_type = ContentTypeChoiceField(
        queryset=ContentType.objects.all(),
        limit_choices_to=ASSIGNEMENT_MODELS,
        label=_('object type'),
    )

    contract = DynamicModelChoiceField(
        queryset=Contract.objects.all(),
        selector=True,
        label=_('Contract'))

    class Meta:
        model = ContractAssignment
        fields = ['content_type', 'contract', 'tags']
        # widgets = {
        #     'content_type': forms.HiddenInput(),
        #     'object_id': forms.HiddenInput(),
        # }

class ContractAssignmentFilterForm(NetBoxModelFilterSetForm):
    model = ContractAssignment
    contract = DynamicModelChoiceField(
        queryset=Contract.objects.all(),
        required=False,
        selector=True,
        label=_('Contract'),
    )

class ContractAssignmentImportForm(NetBoxModelImportForm):
    content_type = CSVContentTypeField(
        queryset=ContentType.objects.all(),
        limit_choices_to=ASSIGNEMENT_MODELS,
        help_text='Content Type in the form <app>.<model>',
        label=_('Content type'),
    )
    contract = CSVModelChoiceField(
        queryset=Contract.objects.all(),
        help_text='Contract id',
        label=_('Contract'),
    )

    class Meta:
        model = ContractAssignment
        fields = ['content_type', 'contract', 'tags']

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

    content_type = ContentTypeChoiceField(
        queryset=ContentType.objects.all(),
        limit_choices_to=ASSIGNEMENT_MODELS,
        label=_('object type'),
    )

    contract = DynamicModelChoiceField(
        queryset=Contract.objects.all(),
        selector=True,
        label=_('Service Level Agreement'))

    class Meta:
        model = ServiceLevelAgreement
        fields = ['content_type', 'contract', 'tags']
        # widgets = {
        #     'content_type': forms.HiddenInput(),
        #     'object_id': forms.HiddenInput(),
        # }

class ServiceLevelAgreementFilterForm(NetBoxModelFilterSetForm):
    model = ContractAssignment
    contract = DynamicModelChoiceField(
        queryset=ServiceLevelAgreement.objects.all(),
        required=False,
        selector=True,
        label=_('ServiceLevelAgreement'),
    )

class ServiceLevelAgreementImportForm(NetBoxModelImportForm):
    content_type = CSVContentTypeField(
        queryset=ContentType.objects.all(),
        limit_choices_to=ASSIGNEMENT_MODELS,
        help_text='Content Type in the form <app>.<model>',
        label=_('Content type'),
    )
    contract = CSVModelChoiceField(
        queryset=ServiceLevelAgreement.objects.all(),
        help_text='ServiceLevelAgreement id',
        label=_('ServiceLevelAgreement'),
    )

    class Meta:
        model = ServiceLevelAgreement
        fields = ['content_type', 'contract', 'tags']

class CServiceLevelAgreementBulkEditForm(NetBoxModelBulkEditForm):
    contract = DynamicModelChoiceField(
        queryset=ServiceLevelAgreement.objects.all(),
        required=False,
        selector=True,
        label=_('Service Level Agreement'),
    )
    model = ServiceLevelAgreement



