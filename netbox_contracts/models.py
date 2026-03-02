from datetime import timedelta

from dcim.choices import DeviceStatusChoices, SiteStatusChoices
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from netbox.choices import ColorChoices
from netbox.models import NetBoxModel
from netbox.models.features import ContactsMixin
from utilities.choices import ChoiceSet
from utilities.fields import ColorField
from virtualization.choices import VirtualMachineStatusChoices


class StatusChoices(ChoiceSet):
    key = 'Contract.status'

    STATUS_ACTIVE = 'active'
    STATUS_CANCELED = 'canceled'
    STATUS_EXPIRED = 'expired'

    CHOICES = [
        (STATUS_ACTIVE, 'Active', 'green'),
        (STATUS_CANCELED, 'Canceled', 'red'),
        (STATUS_EXPIRED, 'Expired', 'orange'),
    ]

class CurrencyChoices(ChoiceSet):
    key = 'Contract.currency'
    CURRENCY_USD = 'usd'

    CHOICES = [
        (CURRENCY_USD, 'USD'),
        ('eur', 'EUR'),
        ('chf', 'CHF'),
    ]
class InternalEntityChoices(ChoiceSet):
    key = 'Contract.internal_party'

    ENTITY = 'Default entity'

    CHOICES = [
        (ENTITY, 'Default entity', 'green'),
    ]

CURRENCY_DEFAULT = CurrencyChoices.CHOICES[0][0]

class ContractType(NetBoxModel):
    name = models.CharField(max_length=100, unique=True, verbose_name=_('name'))
    description = models.TextField(blank=True, verbose_name=_('description'))
    color = ColorField(default=ColorChoices.COLOR_GREY, verbose_name=_('color'))

    class Meta:
        ordering = ('name',)
        verbose_name = _('contract type')
        verbose_name_plural = _('contract types')

    def __str__(self):
        return self.name

    def get_color(self):
        return self.color

    def get_absolute_url(self):
        return reverse('plugins:netbox_contracts:contracttype', args=[self.pk])

class ContractAssignment(NetBoxModel):
    content_type = models.ForeignKey(to=ContentType, on_delete=models.CASCADE, verbose_name=_('content type'))
    content_object = GenericForeignKey(ct_field='content_type', fk_field='object_id')
    contract = models.ForeignKey(
        to='Contract',
        on_delete=models.CASCADE,
        related_name='assignments',
        verbose_name=_('contract'),
    )
    start_date = models.DateField(blank=True, null=True, verbose_name=_('start date'))
    end_date = models.DateField(blank=True, null=True, verbose_name=_('end date'))
    recurring_costs = models.DecimalField(
        verbose_name=_('monthly recuring cost for this assignment'),
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text=_('Enter the monthly recurring cost for this assignment'),
    )
    sla = models.ForeignKey(
        to='ServiceLevelAgreement',
        on_delete=models.PROTECT,
        related_name='+',
        blank=True,
        null=True
    )
    onsite_fe = models.BooleanField(default=False)
    fe_vendor = models.ForeignKey(
        to='circuits.Providers',
        on_delete=models.PROTECT,
        related_name='+',
        blank=True,
        null=True
    )
    clone_fields = ('content_type', 'object_id', 'contract')

    class Meta:
        ordering = ('contract',)
        verbose_name = _('contract assignment')
        verbose_name_plural = _('contract assignments')

    def get_absolute_url(self):
        return reverse('plugins:netbox_contracts:contractassignment', args=[self.pk])

    def get_contract__status_color(self):
        return StatusChoices.colors.get(self.contract.status)

    def get_content_object__status_color(self):
        STATUS_MAPPING = {
            'virtualmachine': VirtualMachineStatusChoices.colors,
            'device': DeviceStatusChoices.colors,
            'site': SiteStatusChoices.colors,
        }
        status_colors = STATUS_MAPPING.get(self.content_type.model, StatusChoices.colors)
        return status_colors.get(self.content_object.status)

class Contract(ContactsMixin, NetBoxModel):
    name = models.CharField(max_length=100, verbose_name=_('name'))
    contract_type = models.ForeignKey(
        to='netbox_contracts.ContractType',
        on_delete=models.PROTECT,
        related_name='contracts',
        blank=True,
        null=True,
        verbose_name=_('contract type'),
    )
    provider = models.ForeignKey(
        to='circuits.Providers',
        on_delete=models.PROTECT,
        related_name='+',
        blank=True,
        null=True
    )
    provider_account = models.ForeignKey(
        to='circuits.ProviderAccounts',
        on_delete=models.PROTECT,
        related_name='+',
        blank=True,
        null=True
    )
    status = models.CharField(
        max_length=50,
        choices=StatusChoices,
        default=StatusChoices.STATUS_ACTIVE,
        verbose_name=_('status'),
    )
    start_date = models.DateField(blank=True, null=True, verbose_name=_('start date'))
    end_date = models.DateField(blank=True, null=True, verbose_name=_('end date'))
    term = models.IntegerField(
        help_text=_('In months'),
        default=12,
        blank=True,
        null=True,
        verbose_name=_('term'),
    )
    notice_period = models.IntegerField(
        help_text=_('Contract notice period. Default to 90 days'),
        default=90,
        verbose_name=_('notice period'),
    )
    currency = models.CharField(
        max_length=3,
        choices=CurrencyChoices,
        default=CURRENCY_DEFAULT,
        verbose_name=_('currency'),
    )
    mrc = models.DecimalField(
        verbose_name=_('monthly recuring cost'),
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text=_('Use either this field of the yearly recuring cost field'),
    )
    nrc = models.DecimalField(verbose_name=_('none recuring cost'), default=0, max_digits=10, decimal_places=2)
    documents = models.URLField(
        blank=True,
        verbose_name=_('documents'),
        help_text=_('URL to the contract documents'),
    )
    comments = models.TextField(blank=True, verbose_name=_('comments'))
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='childs',
        null=True,
        blank=True,
        verbose_name=_('parent'),
    )

    def get_absolute_url(self):
        return reverse('plugins:netbox_contracts:contract', args=[self.pk])

    def get_status_color(self):
        return StatusChoices.colors.get(self.status)

    class Meta:
        ordering = ('name',)
        verbose_name = _('contract')
        verbose_name_plural = _('contracts')

    @property
    def notice_date(self):
        return self.end_date - timedelta(days=self.notice_period)

    def __str__(self):
        return self.name

    def contract_length(self):
        if self.start_date:
            return self.end_date - self.start_date
        return None
    
class ServiceLevelAgreement(NetBoxModel):
    name = models.CharField(max_length=100, verbose_name=_('name'))
    description = models.TextField(blank=True, verbose_name=_('description'))

    class Meta:
        ordering = ('-name',)
        verbose_name = _('SLA')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('plugins:netbox_contracts:servicelevelagreements', args=[self.pk])
