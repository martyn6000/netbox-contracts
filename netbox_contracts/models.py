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
from dcim.models import Region

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

class Currency(NetBoxModel):
    currency_code = models.CharField(
        max_length = 3,
        verbose_name=_('currency code')
    )
    country = models.ForeignKey(
        to=Region,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    currency_name = models.CharField(
        max_length = 100,
        verbose_name=_('currency name')
    )
    currency_number = models.CharField(
        max_length=3,
        verbose_name=('currency number')
    )
    usd_rate = models.DecimalField(
        decimal_places=2,
        max_digits=8,
        null=True,
        blank=True,
        help_text=_('The exchange rate to convert the currency into USD.')
    )

    class Meta:
        ordering = ('currency_code',)

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
    currency = models.ForeignKey(
        to=Currency,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='contract_assignments',
        verbose_name=_('currency'),
        help_text=_('Currency for this contract assignment')
    )
    yrc = models.DecimalField(
            verbose_name=_('yearly recurring cost'),
            max_digits=10,
            decimal_places=2,
            blank=True,
            null=True,
            help_text=_('Enter the yearly recurring Costs'),
        )
    nrc = models.DecimalField(
        verbose_name=_('non recurring cost'), 
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
    provider_account = models.ForeignKey(
            to=Provider,
            on_delete=models.PROTECT,
            related_name='provideraccount',
            blank=True,
            null=True
        )
    fe = models.ForeignKey(
            to=Provider,
            on_delete=models.PROTECT,
            related_name='fe',
            blank=True,
            null=True,
            verbose_name=_('field engineer provider'),
            help_text=_('Field Engineer provider responsible for this assignment'),
        )
    fe_account = models.ForeignKey(
        to=ProviderAccount,
        on_delete=models.PROTECT,
        related_name='feaccount',
        blank=True,
        null=True,
        verbose_name=_('field engineer account'),
        help_text=_('Field Engineer account details'),
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
        'fe',
        'fe_account',
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
        blank=False,
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
    currency = models.ForeignKey(
        to=Currency,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text=_('Enter the local currency for the contract')
    )
    yrc = models.DecimalField(
        verbose_name=_('yearly recurring cost'),
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text=_('Enter the yearly recurring Costs'),
    )
    nrc = models.DecimalField(
        verbose_name=_('non recurring cost'), 
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

    @property
    def usd_yrc_costs(self):
        usd_yrc = self.currency.usd_rate * self.yrc
        return usd_yrc

    @property
    def usd_nrc_costs(self):
        usd_nrc = self.currency.usd_rate * self.nrc
        return usd_nrc

    @property
    def nrc_usd(self):
        if self.nrc is None or self.currency is None or self.currency.usd_rate is None:
            return None

        return self.nrc * self.currency.usd_rate
    
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

    @property
    def contract_status(self):
        today = date.today()
        start = self.start_date
        end = self.end_date
        
        if not start:
            return "Unknown"

        if today < start:
            return "Future"
        elif today > end:
            return "Expired"
        else:
            return "Active"

    @property
    def yrc_usd(self):
        if not self.yrc or not self.currency or not self.currency.usd_rate:
            return None

        return self.yrc * self.currency.usd_rate

    def get_contract_status_color(self):
        return StatusChoices.colors.get(self.contract_status)
