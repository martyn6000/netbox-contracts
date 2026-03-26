from datetime import timedelta, date
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from netbox.choices import ColorChoices
from netbox.models import NetBoxModel
from netbox.models.features import ContactsMixin
from utilities.choices import ChoiceSet
from utilities.fields import ColorField
from circuits.models import Provider, ProviderAccount


class StatusChoices(ChoiceSet):
    ACTIVE = 'Active'
    EXPIRED = 'Expired'
    FUTURE = 'Future'
    UNKNOWN = 'Unknown'

    CHOICES = [
        (ACTIVE, 'Active', 'green'),
        (EXPIRED, 'Expired', 'red'),
        (FUTURE, 'Future', 'blue'),
        (UNKNOWN,'Unknown','gray'),
    ]

class CurrencyChoices(ChoiceSet):
    key = 'Contract.currency'
    CURRENCY_USD = 'usd'

    CHOICES = [
        (CURRENCY_USD, 'USD'),
        ('eur', 'EUR'),
        ('chf', 'CHF'),
    ]

CURRENCY_DEFAULT = CurrencyChoices.CHOICES[0][0]

class ContractType(NetBoxModel):
    name = models.CharField(
        max_length=100, 
        unique=True, 
        verbose_name=_('name')
    )
    description = models.TextField(
        blank=True,
        verbose_name=_('description'),
    )
    color = ColorField(
        default=ColorChoices.COLOR_GREY, 
        verbose_name=_('color'),
        blank=True,
        null=True
    )
    comments = models.TextField(
        blank=True
    )
    
    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_color(self):
        return self.color

class ServiceLevelAgreement(NetBoxModel):
    name = models.CharField(
        max_length=100, 
        verbose_name=_('name')
    )
    description = models.TextField(
        blank=True, 
        verbose_name=_('description')
    )
    comments = models.TextField(
        blank=True
    )
    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

class ContractAssignment(NetBoxModel):
    contract = models.ForeignKey(
        to='Contract',
        on_delete=models.CASCADE,
        related_name='assignments',
        verbose_name=_('contract'),
    )
    object_type = models.ForeignKey(
        to=ContentType,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name=_('object type'),
    )
    object_id = models.PositiveBigIntegerField(
        blank=True,
        null=True,
        verbose_name=_('object ID')
    )
    object = GenericForeignKey(
        ct_field='object_type', 
        fk_field='object_id',
    )
    object.editable = True
    end_date = models.DateField(
        blank=True,
        null=True,
        verbose_name=_('end date'),        
        help_text=_('A unique end date varying from the contract'),
        )
    yrc = models.DecimalField(
            verbose_name=_('yearly recuring cost'),
            max_digits=10,
            decimal_places=2,
            blank=True,
            null=True,
            help_text=_('Enter the yearly recurring Costs'),
        )
    nrc = models.DecimalField(
        verbose_name=_('non recuring cost'), 
        default=0, 
        max_digits=10, 
        decimal_places=2,
        help_text=_('Enter the non recurring costs'),
        blank=True,
    )
    sla = models.ForeignKey(
        to=ServiceLevelAgreement,
        on_delete=models.CASCADE,
        related_name='sla',
        blank=True,
        null=True
    )
    provider = models.ForeignKey(
            to=Provider,
            on_delete=models.PROTECT,
            related_name='provider',
            blank=True,
            null=True
        )
    fe_vendor = models.ForeignKey(
            to=Provider,
            on_delete=models.CASCADE,
            related_name='vendor',
            blank=True,
            null=True
        )
    fe_vendor_account = models.ForeignKey(
        to=ProviderAccount,
        on_delete=models.PROTECT,
        related_name='vendoraccount',
        blank=True,
        null=True
    )
    comments = models.TextField(
        blank=True,
    )
    clone_fields = (
        'contract',
        'end_date',
        'yrc',
        'nrc',
        'sla',
        'fe_vendor',
        'fe_vendor_account',
    )

    class Meta:
        ordering = ('contract',)

    def get_absolute_url(self):
        return reverse(
            'plugins:netbox_contracts:contractassignment', args=[self.pk]
        )

    @property
    def assignment_status(self):
        today = date.today()
        start = self.contract.start_date

        if not self.end_date:
            end = self.contract.end_date
        else:
            end = self.end_date
        
        if not start:
            return "Unknown"

        if today < start:
            return "Future"
        elif today > end:
            return "Expired"
        else:
            return "Active"

    def get_assignment_status_color(self):
        return StatusChoices.colors.get(self.assignment_status)

class Contract(ContactsMixin,NetBoxModel):
    name = models.CharField(
        max_length=100, 
        verbose_name=_('name')
    )
    contract_type = models.ForeignKey(
        to='netbox_contracts.ContractType',
        on_delete=models.PROTECT,
        related_name='contracts',
        blank=True,
        null=True,
        verbose_name=_('contract type'),
    )
    provider = models.ForeignKey(
        to=Provider,
        on_delete=models.PROTECT,
        related_name='providers',
        blank=True,
        null=True
    )
    provider_account = models.ForeignKey(
        to=ProviderAccount,
        on_delete=models.PROTECT,
        related_name='provisderaccounts',
        blank=True,
        null=True
    )
    start_date = models.DateField(
        blank=True, 
        null=True, 
        verbose_name=_('start date')
    )
    end_date = models.DateField(
        blank=True,
        null=True, 
        verbose_name=_('end date')
    )
    notice_period = models.IntegerField(
        help_text=_('Contract notice period. Default to 90 days'),
        default=90,
        verbose_name=_('notice period'),
        blank=True,
        null=True
    )
    currency = models.CharField(
        max_length=3,
        choices=CurrencyChoices,
        default=CURRENCY_DEFAULT,
        verbose_name=_('currency'),
        blank=True,
    )
    yrc = models.DecimalField(
        verbose_name=_('yearly recuring cost'),
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text=_('Enter the yearly recurring Costs'),
    )
    nrc = models.DecimalField(
        verbose_name=_('non recuring cost'), 
        default=0, 
        max_digits=10, 
        decimal_places=2,
        blank=True,
        null=True,
    )
    documents = models.URLField(
        blank=True,
        verbose_name=_('documents'),
        help_text=_('URL to the contract documents'),
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='childs',
        null=True,
        blank=True,
        verbose_name=_('parent'),
    )
    comments = models.TextField(
        blank=True,
    )
    clone_fields = ('contract_type', 'provider', 'provider_account', 'start_date', 'end_date', 'notice_period','currency', 'yrc', 'nrc', 'parent', 'documents' )

    def notice_date(self):
        return self.end_date - timedelta(days=self.notice_period)

    def contract_length(self):
        if self.start_date:
            return self.end_date - self.start_date
        return None

    @property
    def contract_status(self):
        today = date.today()
        if not self.start_date or not self.end_date:
            return "N/A"

        if today < self.start_date:
            return "Upcoming"
        elif today > self.end_date:
            return "Expired"
        else:
            return "Active"

    @property
    def calculated_contract_status_color(self):
        status = self.contract_status
        if status == "Active":
            return "green"
        elif status == "Upcoming":
            return "blue"
        elif status == "Expired":
            return "red"
        else:
            return "gray"

    class Meta:
        ordering = ['name',]
        constraints = (
            models.UniqueConstraint(
                'provider',
                models.functions.Lower('name'),
                name='%(app_label)s_%(class)s_unique_provider_name', # name='%(app_label)s_%(class)s_unique_vendor_contract_id',
                violation_error_message="Contract must be unique per provider.",
            ),
        )

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('plugins:netbox_contracts:contract', args=[self.pk])
