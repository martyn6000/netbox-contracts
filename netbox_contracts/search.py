from netbox.search import SearchIndex

from .models import Contract, ContractType, ServiceLevelAgreement


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


indexes = [
    ServiceLevelAgreementIndex,
    ContractIndex,
    ContractTypeIndex,
]
