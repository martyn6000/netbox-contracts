from typing import TYPE_CHECKING, Annotated

import strawberry
import strawberry_django

from .models import Currency, LicenseAssignment, LicenseType, SoftwareLicense

if TYPE_CHECKING:
    from netbox.graphql.types import ContentTypeType


@strawberry_django.type(
    Currency,
    fields='__all__',
)
class CurrencyType:
    """GraphQL type for Currency model."""

    pass


@strawberry_django.type(
    LicenseType,
    fields='__all__',
)
class LicenseTypeType:
    """GraphQL type for LicenseType model."""

    # The custom ColorField is not in strawberry_django's automatic field mapping
    color: str


@strawberry_django.type(
    SoftwareLicense,
    fields='__all__',
)
class SoftwareLicenseType:
    """GraphQL type for SoftwareLicense model."""

    @strawberry_django.field
    def assignment_count(self) -> int:
        return self.assignment_count


@strawberry_django.type(
    LicenseAssignment,
    fields='__all__',
)
class LicenseAssignmentType:
    """GraphQL type for LicenseAssignment model."""

    object_type: Annotated['ContentTypeType', strawberry.lazy('netbox.graphql.types')] | None


@strawberry.type(name='Query')
class ContractsSoftwareQuery:
    """GraphQL queries for currencies and software licensing."""

    currency: CurrencyType = strawberry_django.field()
    currency_list: list[CurrencyType] = strawberry_django.field()

    license_type: LicenseTypeType = strawberry_django.field()
    license_type_list: list[LicenseTypeType] = strawberry_django.field()

    software_license: SoftwareLicenseType = strawberry_django.field()
    software_license_list: list[SoftwareLicenseType] = strawberry_django.field()

    license_assignment: LicenseAssignmentType = strawberry_django.field()
    license_assignment_list: list[LicenseAssignmentType] = strawberry_django.field()


schema = [
    ContractsSoftwareQuery,
]
