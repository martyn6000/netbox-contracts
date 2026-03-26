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
from .constants import ASSIGNEMENT_MODELS
from .models import (
    Contract,
    ContractAssignment,
    ContractType,
    CurrencyChoices,
    ServiceLevelAgreement,
)
from netbox.forms.mixins import OwnerMixin, OwnerFilterMixin

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

class PrimaryModelFilterSetForm(OwnerFilterMixin, NetBoxModelFilterSetForm):
    """
    FilterSet form for models which inherit from PrimaryModel.
    """
    pass

# Contract
class ContractForm(NetBoxModelForm):
    parent = DynamicModelChoiceField(
        queryset=Contract.objects.all(),
        required=False,
        selector=True,
        label=_('Parent'),
    )
    contract_type = DynamicModelChoiceField(
        queryset=ContractType.objects.all(), required=False, selector=True, label=_('Contract type')
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

    class Meta:
        model = Contract
        fields = [
            'name',
            'contract_type',
            'provider',
            'start_date',
            'end_date',
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

# Circuit Provider forms
# class ProviderForm(PrimaryModelForm):
#     slug = SlugField()
#     asns = DynamicModelMultipleChoiceField(
#         queryset=ASN.objects.all(),
#         label=_('ASNs'),
#         required=False
#     )

#     fieldsets = (
#         FieldSet('name', 'slug', 'asns', 'description', 'tags'),
#     )

#     class Meta:
#         model = Provider
#         fields = [
#             'name', 'slug', 'asns', 'description', 'owner', 'comments', 'tags',
#         ]

# class ProviderAccountForm(PrimaryModelForm):
#     provider = DynamicModelChoiceField(
#         label=_('Provider'),
#         queryset=Provider.objects.all(),
#         selector=True,
#         quick_add=True
#     )

#     class Meta:
#         model = ProviderAccount
#         fields = [
#             'provider', 'name', 'account', 'description', 'owner', 'comments', 'tags',
#         ]

# class ProviderFilterForm(ContactModelFilterForm, PrimaryModelFilterSetForm):
#     model = Provider
#     fieldsets = (
#         FieldSet('q', 'filter_id', 'tag'),
#         FieldSet('region_id', 'site_group_id', 'site_id', name=_('Location')),
#         FieldSet('asn_id', name=_('ASN')),
#         FieldSet('owner_group_id', 'owner_id', name=_('Ownership')),
#         FieldSet('contact', 'contact_role', 'contact_group', name=_('Contacts')),
#     )
#     region_id = DynamicModelMultipleChoiceField(
#         queryset=Region.objects.all(),
#         required=False,
#         label=_('Region')
#     )
#     site_group_id = DynamicModelMultipleChoiceField(
#         queryset=SiteGroup.objects.all(),
#         required=False,
#         label=_('Site group')
#     )
#     site_id = DynamicModelMultipleChoiceField(
#         queryset=Site.objects.all(),
#         required=False,
#         query_params={
#             'region_id': '$region_id',
#             'site_group_id': '$site_group_id',
#         },
#         label=_('Site')
#     )
#     asn_id = DynamicModelMultipleChoiceField(
#         queryset=ASN.objects.all(),
#         required=False,
#         label=_('ASNs')
#     )
#     tag = TagFilterField(model)

# class ProviderAccountFilterForm(ContactModelFilterForm, PrimaryModelFilterSetForm):
#     model = ProviderAccount
#     fieldsets = (
#         FieldSet('q', 'filter_id', 'tag'),
#         FieldSet('provider_id', 'account', name=_('Attributes')),
#         FieldSet('owner_group_id', 'owner_id', name=_('Ownership')),
#         FieldSet('contact', 'contact_role', 'contact_group', name=_('Contacts')),
#     )
#     provider_id = DynamicModelMultipleChoiceField(
#         queryset=Provider.objects.all(),
#         required=False,
#         label=_('Provider')
#     )
#     account = forms.CharField(
#         label=_('Account'),
#         required=False
#     )
#     tag = TagFilterField(model)

# class ProviderBulkEditForm(PrimaryModelBulkEditForm):
#     asns = DynamicModelMultipleChoiceField(
#         queryset=ASN.objects.all(),
#         label=_('ASNs'),
#         required=False
#     )

#     model = Provider
#     fieldsets = (
#         FieldSet('asns', 'description'),
#     )
#     nullable_fields = (
#         'asns', 'description', 'comments',
#     )

# class ProviderAccountBulkEditForm(PrimaryModelBulkEditForm):
#     provider = DynamicModelChoiceField(
#         label=_('Provider'),
#         queryset=Provider.objects.all(),
#         required=False
#     )

#     model = ProviderAccount
#     fieldsets = (
#         FieldSet('provider', 'description'),
#     )
#     nullable_fields = (
#         'description', 'comments',
#     )

# ContractAssignment
class ContractAssignmentForm(NetBoxModelForm):

    object_type = ContentTypeChoiceField(
        queryset=ContentType.objects.all(),
        limit_choices_to=ASSIGNEMENT_MODELS,
        widget=HTMXSelect(),
        label=_('Object Type'),
    )
    object = forms.ModelChoiceField(
        queryset=None, 
        label=_('Object')
    )
    fe_vendor = DynamicModelChoiceField(
        label=_('FE Vendor'),
        queryset=Provider.objects.all(),
    ) 
    fe_vendor_account = DynamicModelChoiceField(
        label=_('FE Vendor account'),
        queryset=ProviderAccount.objects.all(),
        required=False,
        query_params={
            'provider_id': '$fe_vendor',
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
            'fe_vendor',
            'fe_vendor_account',
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
    fe_vendor = DynamicModelChoiceField(
        queryset=Provider.objects.all(),
        required=False,
        selector=True,
        label=_('FE Vendor'),
        help_text=_('Filter by FE Vendor'),
    )
    fe_vendor_account = DynamicModelChoiceField(
        queryset=ProviderAccount.objects.all(),
        required=False,
        selector=True,
        label=_('FE Vendor Account'),
        help_text=_('Filter by FE Vendor Account'),
        query_params={
            'provider_id': '$fe_vendor',
        }
    )

class ContractAssignmentImportForm(NetBoxModelImportForm):
    object_type = CSVContentTypeField(
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
        fields = ['object_type', 'contract', 'tags']

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
    object_type = CSVContentTypeField(
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
        fields = ['object_type', 'contract', 'tags']

class ServiceLevelAgreementBulkEditForm(NetBoxModelBulkEditForm):
    contract = DynamicModelChoiceField(
        queryset=ServiceLevelAgreement.objects.all(),
        required=False,
        selector=True,
        label=_('Service Level Agreement'),
    )
    model = ServiceLevelAgreement

