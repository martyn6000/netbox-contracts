"""
Test cases for SCB Netbox contract plugin models.
"""

from dcim.models import Manufacturer, Site
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError

from ..models import Currency, LicenseAssignment, LicenseType, SoftwareLicense
from ..testing import PluginModelTestCase
from ..testing.utils import create_tags, get_random_string


class LicenseTypeTestCase(PluginModelTestCase):
    """Test LicenseType model."""

    @classmethod
    def setUpTestData(cls):
        LicenseType.objects.create(name='Perpetual', description='Perpetual license', color='2196f3')
        LicenseType.objects.create(name='Subscription', description='Subscription license', color='4caf50')
        LicenseType.objects.create(name='Trial', color='ffc107')

    def test_create_license_type(self):
        name = f'Type {get_random_string(10)}'
        instance = LicenseType.objects.create(name=name, color='9e9e9e')

        self.assertEqual(instance.name, name)
        self.assertIsNotNone(instance.pk)

    def test_license_type_str(self):
        instance = LicenseType.objects.first()
        self.assertEqual(str(instance), instance.name)

    def test_license_type_absolute_url(self):
        instance = LicenseType.objects.first()
        url = instance.get_absolute_url()

        self.assertIsNotNone(url)
        self.assertIn(str(instance.pk), url)

    def test_license_type_unique_name(self):
        name = 'Duplicate Type'
        LicenseType.objects.create(name=name)

        with self.assertRaises(ValidationError):
            instance = LicenseType(name=name)
            instance.full_clean()

    def test_license_type_default_color(self):
        instance = LicenseType.objects.create(name=f'Type {get_random_string(10)}')
        self.assertTrue(instance.color)

    def test_license_type_with_tags(self):
        tags = create_tags(['important', 'test'])
        instance = LicenseType.objects.first()

        instance.tags.add(*tags)
        instance.save()

        self.assertEqual(instance.tags.count(), 2)
        self.assertIn(tags[0], instance.tags.all())

    def test_ordering(self):
        instances = list(LicenseType.objects.all())
        names = [instance.name for instance in instances]
        self.assertEqual(names, sorted(names))


class LicenseTypeValidationTestCase(PluginModelTestCase):
    """Test LicenseType validation."""

    def test_empty_name(self):
        with self.assertRaises(ValidationError):
            instance = LicenseType(name='')
            instance.full_clean()

    def test_name_max_length(self):
        long_name = 'x' * 101  # Exceeds max_length of 100

        with self.assertRaises(ValidationError):
            instance = LicenseType(name=long_name)
            instance.full_clean()


class SoftwareLicenseTestCase(PluginModelTestCase):
    """Test SoftwareLicense model."""

    @classmethod
    def setUpTestData(cls):
        cls.manufacturer = Manufacturer.objects.create(name='Acme Corp', slug='acme-corp')
        cls.license_type = LicenseType.objects.create(name='Subscription')

        SoftwareLicense.objects.create(
            manufacturer=cls.manufacturer,
            license_name='Acme Office Suite',
            friendly_name='Office Suite',
            license_sku='ACME-OFFICE-001',
            per_license_cost='19.99',
            license_type=cls.license_type,
        )
        SoftwareLicense.objects.create(
            manufacturer=cls.manufacturer,
            license_name='Acme Design Tool',
            license_sku='ACME-DESIGN-001',
            per_license_cost='49.50',
        )

    def test_create_software_license(self):
        license_name = f'License {get_random_string(10)}'
        instance = SoftwareLicense.objects.create(
            manufacturer=self.manufacturer,
            license_name=license_name,
            license_sku=get_random_string(10),
            license_type=self.license_type,
        )

        self.assertEqual(instance.license_name, license_name)
        self.assertIsNotNone(instance.pk)

    def test_software_license_str(self):
        instance = SoftwareLicense.objects.first()
        self.assertEqual(str(instance), instance.license_name)

    def test_software_license_absolute_url(self):
        instance = SoftwareLicense.objects.first()
        url = instance.get_absolute_url()

        self.assertIsNotNone(url)
        self.assertIn(str(instance.pk), url)

    def test_assignment_count_with_no_assignments(self):
        instance = SoftwareLicense.objects.get(license_name='Acme Design Tool')
        self.assertEqual(instance.assignment_count, 0)

    def test_assignment_count_reflects_assignments(self):
        instance = SoftwareLicense.objects.get(license_name='Acme Office Suite')
        site_type = ContentType.objects.get_for_model(Site)
        site_1 = Site.objects.create(name='Site 1', slug='site-1')
        site_2 = Site.objects.create(name='Site 2', slug='site-2')

        LicenseAssignment.objects.create(software_license=instance, object_type=site_type, object_id=site_1.pk)
        self.assertEqual(instance.assignment_count, 1)

        LicenseAssignment.objects.create(software_license=instance, object_type=site_type, object_id=site_2.pk)
        self.assertEqual(instance.assignment_count, 2)

    def test_local_currency_is_optional(self):
        instance = SoftwareLicense.objects.get(license_name='Acme Design Tool')
        self.assertIsNone(instance.local_currency)

    def test_local_currency_link(self):
        currency = Currency.objects.create(currency_code='GBP', currency_name='Pound Sterling', currency_number='826')
        instance = SoftwareLicense.objects.get(license_name='Acme Design Tool')
        instance.local_currency = currency
        instance.save()

        instance.refresh_from_db()
        self.assertEqual(instance.local_currency.currency_code, 'GBP')
        self.assertIn(instance, currency.software_licenses.all())

    def test_deleting_currency_keeps_license(self):
        currency = Currency.objects.create(currency_code='EUR', currency_name='Euro', currency_number='978')
        instance = SoftwareLicense.objects.get(license_name='Acme Design Tool')
        instance.local_currency = currency
        instance.save()

        currency.delete()

        instance.refresh_from_db()
        self.assertIsNone(instance.local_currency)

    def test_software_license_optional_fields(self):
        instance = SoftwareLicense.objects.get(license_name='Acme Design Tool')

        self.assertEqual(instance.friendly_name, '')
        self.assertIsNone(instance.license_type)

    def test_per_license_cost_precision(self):
        instance = SoftwareLicense.objects.get(license_name='Acme Office Suite')
        self.assertEqual(str(instance.per_license_cost), '19.99')

    def test_manufacturer_relation(self):
        instance = SoftwareLicense.objects.first()
        self.assertIn(instance, self.manufacturer.software_licenses.all())

    def test_license_type_relation(self):
        instance = SoftwareLicense.objects.get(license_name='Acme Office Suite')
        self.assertIn(instance, self.license_type.software_licenses.all())

    def test_software_license_with_tags(self):
        tags = create_tags(['important', 'test'])
        instance = SoftwareLicense.objects.first()

        instance.tags.add(*tags)
        instance.save()

        self.assertEqual(instance.tags.count(), 2)
        self.assertIn(tags[0], instance.tags.all())

    def test_ordering(self):
        instances = list(SoftwareLicense.objects.all())
        names = [instance.license_name for instance in instances]
        self.assertEqual(names, sorted(names))


class SoftwareLicenseValidationTestCase(PluginModelTestCase):
    """Test SoftwareLicense validation."""

    @classmethod
    def setUpTestData(cls):
        cls.manufacturer = Manufacturer.objects.create(name='Acme Corp', slug='acme-corp')

    def test_manufacturer_required(self):
        with self.assertRaises(ValidationError):
            instance = SoftwareLicense(license_name='Test', license_sku='SKU-1')
            instance.full_clean()

    def test_license_name_required(self):
        with self.assertRaises(ValidationError):
            instance = SoftwareLicense(manufacturer=self.manufacturer, license_sku='SKU-1')
            instance.full_clean()

    def test_license_sku_required(self):
        with self.assertRaises(ValidationError):
            instance = SoftwareLicense(manufacturer=self.manufacturer, license_name='Test')
            instance.full_clean()

    def test_license_name_max_length(self):
        long_name = 'x' * 151  # Exceeds max_length of 150

        with self.assertRaises(ValidationError):
            instance = SoftwareLicense(
                manufacturer=self.manufacturer,
                license_name=long_name,
                license_sku='SKU-1',
            )
            instance.full_clean()


class LicenseAssignmentTestCase(PluginModelTestCase):
    """Test LicenseAssignment model."""

    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(name='Acme Corp', slug='acme-corp')
        cls.software_license = SoftwareLicense.objects.create(
            manufacturer=manufacturer,
            license_name='Acme Office Suite',
            license_sku='ACME-OFFICE-001',
        )
        cls.site_type = ContentType.objects.get_for_model(Site)
        cls.site_1 = Site.objects.create(name='Site 1', slug='site-1')
        cls.site_2 = Site.objects.create(name='Site 2', slug='site-2')

        LicenseAssignment.objects.create(
            software_license=cls.software_license,
            object_type=cls.site_type,
            object_id=cls.site_1.pk,
        )

    def test_create_license_assignment(self):
        instance = LicenseAssignment.objects.create(
            software_license=self.software_license,
            object_type=self.site_type,
            object_id=self.site_2.pk,
        )

        self.assertIsNotNone(instance.pk)
        self.assertEqual(instance.assigned_object, self.site_2)

    def test_license_assignment_str(self):
        instance = LicenseAssignment.objects.first()
        self.assertIn(str(self.software_license), str(instance))
        self.assertIn(str(self.site_1), str(instance))

    def test_license_assignment_absolute_url(self):
        instance = LicenseAssignment.objects.first()
        url = instance.get_absolute_url()

        self.assertIsNotNone(url)
        self.assertIn(str(instance.pk), url)

    def test_assigned_object_resolves(self):
        instance = LicenseAssignment.objects.first()
        self.assertEqual(instance.assigned_object, self.site_1)

    def test_reverse_relation_from_software_license(self):
        instance = LicenseAssignment.objects.first()
        self.assertIn(instance, self.software_license.assignments.all())

    def test_duplicate_assignment_not_allowed(self):
        with self.assertRaises(ValidationError):
            instance = LicenseAssignment(
                software_license=self.software_license,
                object_type=self.site_type,
                object_id=self.site_1.pk,
            )
            instance.full_clean()
            instance.validate_constraints()


class LicenseAssignmentValidationTestCase(PluginModelTestCase):
    """Test LicenseAssignment validation."""

    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(name='Acme Corp', slug='acme-corp')
        cls.software_license = SoftwareLicense.objects.create(
            manufacturer=manufacturer,
            license_name='Acme Office Suite',
            license_sku='ACME-OFFICE-001',
        )
        cls.site_type = ContentType.objects.get_for_model(Site)
        cls.site = Site.objects.create(name='Site 1', slug='site-1')

    def test_software_license_required(self):
        with self.assertRaises(ValidationError):
            instance = LicenseAssignment(object_type=self.site_type, object_id=self.site.pk)
            instance.full_clean()

    def test_object_type_required(self):
        with self.assertRaises(ValidationError):
            instance = LicenseAssignment(software_license=self.software_license, object_id=self.site.pk)
            instance.full_clean()

    def test_object_id_required(self):
        with self.assertRaises(ValidationError):
            instance = LicenseAssignment(software_license=self.software_license, object_type=self.site_type)
            instance.full_clean()
