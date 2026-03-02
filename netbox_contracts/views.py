from datetime import date, timedelta

from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Case, F, When
from django.db.models.functions import Round
from django.shortcuts import get_object_or_404, render
from netbox.views import generic
from netbox.views.generic.utils import get_prerequisite_model
from utilities.forms import restrict_form_fields
from utilities.querydict import normalize_querydict
from utilities.views import register_model_view

from . import filtersets, forms, tables
from .models import (
    Contract,
    ContractAssignment,
    ContractType,
    ServiceLevelAgreement,
)
from circuits.models import (
    Provider,
    ProviderAccount,
)

plugin_settings = settings.PLUGINS_CONFIG['netbox_contracts']

# ContractType views

class ContractTypeView(generic.ObjectView):
    queryset = ContractType.objects.all()

class ContractTypeListView(generic.ObjectListView):
    queryset = ContractType.objects.all()
    table = tables.ContractTypeListTable
    filterset = filtersets.ContractTypeFilterSet
    filterset_form = forms.ContractTypeFilterForm

class ContractTypeEditView(generic.ObjectEditView):
    queryset = ContractType.objects.all()
    form = forms.ContractTypeForm

class ContractTypeBulkImportView(generic.BulkImportView):
    queryset = ContractType.objects.all()
    model_form = forms.ContractTypeCSVForm
    table = tables.ContractTypeListTable

class ContractTypeBulkEditView(generic.BulkEditView):
    queryset = ContractType.objects.annotate()
    filterset = filtersets.ContractTypeFilterSet
    table = tables.ContractTypeListTable
    form = forms.ContractTypeBulkEditForm

class ContractTypeDeleteView(generic.ObjectDeleteView):
    queryset = ContractType.objects.all()

class ContractTypeBulkDeleteView(generic.BulkDeleteView):
    queryset = ContractType.objects.annotate()
    filterset = filtersets.ContractTypeFilterSet
    table = tables.ContractTypeListTable

# Contract assignment view

class ContractAssignmentView(generic.ObjectView):
    queryset = ContractAssignment.objects.all()

class ContractAssignmentListView(generic.ObjectListView):
    queryset = ContractAssignment.objects.all()
    table = tables.ContractAssignmentListTable
    filterset = filtersets.ContractAssignmentFilterSet
    filterset_form = forms.ContractAssignmentFilterForm

class ContractAssignmentEditView(generic.ObjectEditView):
    queryset = ContractAssignment.objects.all()
    form = forms.ContractAssignmentForm

    def alter_object(self, instance, request, args, kwargs):
        if not instance.pk and kwargs:
            # Assign the object based on URL kwargs
            content_type = get_object_or_404(
                ContentType, pk=request.GET.get('content_type')
            )
            instance.object = get_object_or_404(
                content_type.model_class(), pk=request.GET.get('object_id')
            )
        return instance

    def get_extra_addanother_params(self, request):
        return {
            'content_type': request.GET.get('content_type'),
            'object_id': request.GET.get('object_id'),
        }

class ContractAssignmentDeleteView(generic.ObjectDeleteView):
    queryset = ContractAssignment.objects.all()

class ContractAssignmentBulkImportView(generic.BulkImportView):
    queryset = ContractAssignment.objects.all()
    model_form = forms.ContractAssignmentImportForm
    table = tables.ContractAssignmentListTable

class ContractAssignmentBulkEditView(generic.BulkEditView):
    queryset = ContractAssignment.objects.annotate()
    filterset = filtersets.ContractAssignmentFilterSet
    table = tables.ContractAssignmentListTable
    form = forms.ContractAssignmentBulkEditForm

class ContractAssignmentBulkDeleteView(generic.BulkDeleteView):
    queryset = ContractAssignment.objects.annotate()
    filterset = filtersets.ContractAssignmentFilterSet
    table = tables.ContractAssignmentListTable

# Contract views

@register_model_view(Contract)
class ContractView(generic.ObjectView):

    def get_extra_context(self, request, instance):
        invoices_table = tables.InvoiceListTable(
            instance.invoices.exclude(template=True)
        )
        invoices_table.columns.hide('contracts')
        invoices_table.configure(request)
        assignments_table = tables.ContractAssignmentContractTable(
            instance.assignments.all()
        )
        invoice_template = instance.invoices.filter(template=True).first()
        if invoice_template:
            invoicelines_table = tables.InvoiceLineListTable(
                invoice_template.invoicelines.all()
            )
            invoicelines_table.columns.hide('invoice')
            invoicelines_table.columns.hide('currency')
            invoicelines_table.configure(request)
        else:
            invoicelines_table = None
        assignments_table.configure(request)
        if instance.childs.all():
            childs_table = tables.ContractListBottomTable(instance.childs.all())
            childs_table.configure(request)
        else:
            childs_table = None

        hidden_fields = plugin_settings.get('hidden_contract_fields')

        return {
            'hidden_fields': hidden_fields,
            'invoices_table': invoices_table,
            'invoice_template': invoice_template,
            'invoicelines_table': invoicelines_table,
            'assignments_table': assignments_table,
            'childs_table': childs_table,
        }

class ContractListView(generic.ObjectListView):
    table = tables.ContractListTable
    filterset = filtersets.ContractFilterSet
    filterset_form = forms.ContractFilterForm

class ContractEditView(generic.ObjectEditView):
    queryset = Contract.objects.all()
    form = forms.ContractForm

    def alter_object(self, obj, request, url_args, url_kwargs):
        """
        When this method is called after a Post,
        it is used here to set the external party object id for exiting objects,
        In any case, this happens before the form is instanciated.

        Args:
            obj: The object being edited
            request: The current request
            url_args: URL path args
            url_kwargs: URL path kwargs
        """

        if request.method == 'POST':
            data = normalize_querydict(request.POST)
            obj.external_party_object_id = data['external_party_object']
            external_party_object_type_id = data['external_party_object_type']
            obj.external_party_object_type = ContentType.objects.get(
                id=external_party_object_type_id
            )
            external_party_object_type = obj.external_party_object_type
            obj.external_party_object = (
                external_party_object_type.get_object_for_this_type(
                    id=obj.external_party_object_id
                )
            )

        return obj

class ContractDeleteView(generic.ObjectDeleteView):
    queryset = Contract.objects.all()

class ContractBulkImportView(generic.BulkImportView):
    queryset = Contract.objects.all()
    model_form = forms.ContractCSVForm
    table = tables.ContractListTable

class ContractBulkEditView(generic.BulkEditView):
    queryset = Contract.objects.all()
    filterset = filtersets.ContractFilterSet
    table = tables.ContractListTable
    form = forms.ContractBulkEditForm

class ContractBulkDeleteView(generic.BulkDeleteView):
    queryset = Contract.objects.all()
    filterset = filtersets.ContractFilterSet
    table = tables.ContractListTable
  
# Provider views
class ProviderView(generic.ObjectView):
    queryset = Provider.objects.all()

class ProviderListView(generic.ObjectListView):
    queryset = Provider.objects.all()
    table = tables.ProviderListTable
    filterset = filtersets.ProviderFilterSet
    filterset_form = forms.ProviderFilterForm

class ProviderEditView(generic.ObjectEditView):
    queryset = Provider.objects.all()
    form = forms.ProviderForm

class ProviderBulkImportView(generic.BulkImportView):
    queryset = Provider.objects.all()
    model_form = forms.ProviderCSVForm
    table = tables.ProviderListTable

class ProviderBulkEditView(generic.BulkEditView):
    queryset = Provider.objects.annotate()
    filterset = filtersets.ProviderFilterSet
    table = tables.ProviderListTable
    form = forms.ProviderBulkEditForm

class ProviderDeleteView(generic.ObjectDeleteView):
    queryset = Provider.objects.all()

class ProviderBulkDeleteView(generic.BulkDeleteView):
    queryset = Provider.objects.annotate()
    filterset = filtersets.ProviderFilterSet
    table = tables.ProviderListTable
  
# Provider Account views
class ProviderAccountView(generic.ObjectView):
    queryset = ProviderAccount.objects.all()

class ProviderAccountListView(generic.ObjectListView):
    queryset = ProviderAccount.objects.all()
    table = tables.ProviderAccountListTable
    filterset = filtersets.ProviderAccountFilterSet
    filterset_form = forms.ProviderAccountFilterForm

class ProviderAccountEditView(generic.ObjectEditView):
    queryset = ProviderAccount.objects.all()
    form = forms.ProviderAccountForm

class ProviderAccountBulkImportView(generic.BulkImportView):
    queryset = ProviderAccount.objects.all()
    model_form = forms.ProviderAccountCSVForm
    table = tables.ProviderAccountListTable

class ProviderAccountBulkEditView(generic.BulkEditView):
    queryset = ProviderAccount.objects.annotate()
    filterset = filtersets.ProviderAccountFilterSet
    table = tables.ProviderAccountListTable
    form = forms.ProviderAccountBulkEditForm

class ProviderAccountDeleteView(generic.ObjectDeleteView):
    queryset = ProviderAccount.objects.all()

class ProviderAccountBulkDeleteView(generic.BulkDeleteView):
    queryset = ProviderAccount.objects.annotate()
    filterset = filtersets.ProviderAccountFilterSet
    table = tables.ProviderAccountListTable
  
# Service Level Agreement views
class ServiceLevelAgreementView(generic.ObjectView):
    queryset = ServiceLevelAgreement.objects.all()

class ServiceLevelAgreementListView(generic.ObjectListView):
    queryset = ServiceLevelAgreement.objects.all()
    table = tables.ServiceLevelAgreementListTable
    filterset = filtersets.ServiceLevelAgreementFilterSet
    filterset_form = forms.ServiceLevelAgreementFilterForm

class ServiceLevelAgreementEditView(generic.ObjectEditView):
    queryset = ServiceLevelAgreement.objects.all()
    form = forms.ServiceLevelAgreementForm

class ServiceLevelAgreementBulkImportView(generic.BulkImportView):
    queryset = ServiceLevelAgreement.objects.all()
    model_form = forms.ServiceLevelAgreementCSVForm
    table = tables.ServiceLevelAgreementListTable

class ServiceLevelAgreementBulkEditView(generic.BulkEditView):
    queryset = ServiceLevelAgreement.objects.annotate()
    filterset = filtersets.ServiceLevelAgreementFilterSet
    table = tables.ServiceLevelAgreementListTable
    form = forms.ServiceLevelAgreementBulkEditForm

class ServiceLevelAgreementDeleteView(generic.ObjectDeleteView):
    queryset = ServiceLevelAgreement.objects.all()

class ServiceLevelAgreementBulkDeleteView(generic.BulkDeleteView):
    queryset = ServiceLevelAgreement.objects.annotate()
    filterset = filtersets.ServiceLevelAgreementFilterSet
    table = tables.ServiceLevelAgreementListTable

