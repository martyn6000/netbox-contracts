from netbox.search import SearchIndex

from .models import Contract, ContractType, LicenseType, ServiceLevelAgreement, SoftwareLicense


class ServiceLevelAgreementIndex(SearchIndex):
    model = ServiceLevelAgreement
    fields = (
        ('name', 100),
    )


class ContractIndex(SearchIndex):
    model = Contract
    fields = (
        ('name', 100),
        ('comments', 5000),
    )

class ContractTypeIndex(SearchIndex):
    model = ContractType
    fields = (
        ('name', 20),
        ('description', 20),
    )

class LicenseTypeIndex(SearchIndex):
    model = LicenseType
    fields = (
        ('name', 100),
        ('description', 500),
    )
    display_attrs = ('description', 'color')


class SoftwareLicenseIndex(SearchIndex):
    model = SoftwareLicense
    fields = (
        ('license_name', 100),
        ('friendly_name', 200),
        ('license_sku', 50),
    )
    display_attrs = ('manufacturer', 'license_type')


indexes = [
    ServiceLevelAgreementIndex,
    ContractIndex,
    ContractTypeIndex,
    LicenseTypeIndex,
    SoftwareLicenseIndex,
]
