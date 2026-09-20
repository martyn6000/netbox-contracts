"""
Test cases for SCB Netbox contract plugin REST API.
"""

from dcim.models import Manufacturer, Site
from django.contrib.contenttypes.models import ContentType

from ..models import Currency, LicenseAssignment, LicenseType, SoftwareLicense
from ..testing import PluginAPITestCase
from ..testing.utils import disable_warnings, get_random_string


class LicenseTypeAPITestCase(PluginAPITestCase):
    """Test LicenseType API endpoints."""

    @classmethod
    def setUpTestData(cls):
        LicenseType.objects.create(name='API Type 1')
        LicenseType.objects.create(name='API Type 2')
        LicenseType.objects.create(name='API Type 3')

    def setUp(self):
        super().setUp()
        self.list_url_name = 'plugins-api:netbox_contracts-api:licensetype-list'
        self.detail_url_name = 'plugins-api:netbox_contracts-api:licensetype-detail'

    def test_list_license_types(self):
        self.add_permissions('netbox_contracts.view_licensetype')

        url = self._get_list_url()
        response = self.client.get(url)

        self.assertHttpStatus(response, 200)
        self.assertEqual(response.data['count'], 3)

    def test_list_license_types_without_permission(self):
        url = self._get_list_url()

        with disable_warnings('django.request'):
            response = self.client.get(url)
            self.assertHttpStatus(response, 403)

    def test_get_license_type(self):
        self.add_permissions('netbox_contracts.view_licensetype')

        instance = LicenseType.objects.first()
        url = self._get_detail_url(instance)
        response = self.client.get(url)

        self.assertHttpStatus(response, 200)
        self.assertEqual(response.data['id'], instance.pk)
        self.assertEqual(response.data['name'], instance.name)

    def test_create_license_type(self):
        self.add_permissions('netbox_contracts.add_licensetype')

        url = self._get_list_url()
        name = f'API Created {get_random_string(10)}'

        data = {
            'name': name,
            'color': '2196f3',
        }

        response = self.client.post(url, data, format='json')
        self.assertHttpStatus(response, 201)

        instance = LicenseType.objects.get(name=name)
        self.assertEqual(instance.name, name)

    def test_create_license_type_without_permission(self):
        url = self._get_list_url()

        with disable_warnings('django.request'):
            response = self.client.post(url, {'name': 'Test'}, format='json')
            self.assertHttpStatus(response, 403)

    def test_update_license_type(self):
        self.add_permissions('netbox_contracts.change_licensetype')

        instance = LicenseType.objects.first()
        url = self._get_detail_url(instance)
        new_name = f'Updated {get_random_string(10)}'

        response = self.client.patch(url, {'name': new_name}, format='json')
        self.assertHttpStatus(response, 200)

        instance.refresh_from_db()
        self.assertEqual(instance.name, new_name)

    def test_delete_license_type(self):
        self.add_permissions('netbox_contracts.delete_licensetype')

        instance = LicenseType.objects.first()
        url = self._get_detail_url(instance)

        response = self.client.delete(url)
        self.assertHttpStatus(response, 204)

        self.assertFalse(LicenseType.objects.filter(pk=instance.pk).exists())


class SoftwareLicenseAPITestCase(PluginAPITestCase):
    """Test SoftwareLicense API endpoints."""

    @classmethod
    def setUpTestData(cls):
        cls.manufacturer = Manufacturer.objects.create(name='Acme Corp', slug='acme-corp')
        cls.license_type = LicenseType.objects.create(name='Subscription')

        SoftwareLicense.objects.create(
            manufacturer=cls.manufacturer,
            license_name='API License 1',
            license_sku='SKU-1',
            per_license_cost='9.99',
            license_type=cls.license_type,
        )
        SoftwareLicense.objects.create(
            manufacturer=cls.manufacturer,
            license_name='API License 2',
            license_sku='SKU-2',
        )
        SoftwareLicense.objects.create(
            manufacturer=cls.manufacturer,
            license_name='API License 3',
            license_sku='SKU-3',
        )

    def setUp(self):
        super().setUp()
        self.list_url_name = 'plugins-api:netbox_contracts-api:softwarelicense-list'
        self.detail_url_name = 'plugins-api:netbox_contracts-api:softwarelicense-detail'

    def test_list_software_licenses(self):
        self.add_permissions('netbox_contracts.view_softwarelicense')

        url = self._get_list_url()
        response = self.client.get(url)

        self.assertHttpStatus(response, 200)
        self.assertEqual(response.data['count'], 3)

    def test_list_software_licenses_without_permission(self):
        url = self._get_list_url()

        with disable_warnings('django.request'):
            response = self.client.get(url)
            self.assertHttpStatus(response, 403)

    def test_get_software_license(self):
        self.add_permissions('netbox_contracts.view_softwarelicense')

        instance = SoftwareLicense.objects.first()
        url = self._get_detail_url(instance)
        response = self.client.get(url)

        self.assertHttpStatus(response, 200)
        self.assertEqual(response.data['id'], instance.pk)
        self.assertEqual(response.data['license_name'], instance.license_name)

    def test_create_software_license_with_local_currency(self):
        self.add_permissions('netbox_contracts.add_softwarelicense')
        currency = Currency.objects.create(currency_code='GBP', currency_name='Pound Sterling', currency_number='826')

        data = {
            'manufacturer': self.manufacturer.pk,
            'license_name': f'API Currency {get_random_string(10)}',
            'license_sku': get_random_string(10),
            'local_currency': currency.pk,
        }

        response = self.client.post(self._get_list_url(), data, format='json')
        self.assertHttpStatus(response, 201)
        self.assertEqual(response.data['local_currency']['currency_code'], 'GBP')

    def test_assignment_count_in_response(self):
        self.add_permissions('netbox_contracts.view_softwarelicense')

        instance = SoftwareLicense.objects.get(license_name='API License 1')
        site_type = ContentType.objects.get_for_model(Site)
        site = Site.objects.create(name='Site 1', slug='site-1')
        LicenseAssignment.objects.create(software_license=instance, object_type=site_type, object_id=site.pk)

        url = self._get_detail_url(instance)
        response = self.client.get(url)

        self.assertHttpStatus(response, 200)
        self.assertEqual(response.data['assignment_count'], 1)

    def test_create_software_license(self):
        self.add_permissions('netbox_contracts.add_softwarelicense')

        url = self._get_list_url()
        license_name = f'API Created {get_random_string(10)}'

        data = {
            'manufacturer': self.manufacturer.pk,
            'license_name': license_name,
            'license_sku': get_random_string(10),
            'per_license_cost': '14.95',
            'license_type': self.license_type.pk,
        }

        response = self.client.post(url, data, format='json')
        self.assertHttpStatus(response, 201)

        instance = SoftwareLicense.objects.get(license_name=license_name)
        self.assertEqual(instance.license_name, license_name)
        self.assertEqual(response.data['id'], instance.pk)

    def test_create_software_license_without_permission(self):
        url = self._get_list_url()

        with disable_warnings('django.request'):
            response = self.client.post(url, {'license_name': 'Test'}, format='json')
            self.assertHttpStatus(response, 403)

    def test_update_software_license(self):
        self.add_permissions('netbox_contracts.change_softwarelicense')

        instance = SoftwareLicense.objects.first()
        url = self._get_detail_url(instance)
        new_name = f'Updated {get_random_string(10)}'

        response = self.client.patch(url, {'license_name': new_name}, format='json')
        self.assertHttpStatus(response, 200)

        instance.refresh_from_db()
        self.assertEqual(instance.license_name, new_name)

    def test_delete_software_license(self):
        self.add_permissions('netbox_contracts.delete_softwarelicense')

        instance = SoftwareLicense.objects.first()
        url = self._get_detail_url(instance)

        response = self.client.delete(url)
        self.assertHttpStatus(response, 204)

        self.assertFalse(SoftwareLicense.objects.filter(pk=instance.pk).exists())

    def test_options_software_license(self):
        self.add_permissions('netbox_contracts.view_softwarelicense')

        url = self._get_list_url()
        response = self.client.options(url)

        self.assertHttpStatus(response, 200)


class SoftwareLicenseAPIValidationTestCase(PluginAPITestCase):
    """Test SoftwareLicense API validation."""

    @classmethod
    def setUpTestData(cls):
        cls.manufacturer = Manufacturer.objects.create(name='Acme Corp', slug='acme-corp')

    def setUp(self):
        super().setUp()
        self.add_permissions('netbox_contracts.add_softwarelicense')
        self.list_url_name = 'plugins-api:netbox_contracts-api:softwarelicense-list'

    def test_create_with_missing_manufacturer(self):
        url = self._get_list_url()
        data = {'license_name': 'Test', 'license_sku': 'SKU-1'}

        response = self.client.post(url, data, format='json')
        self.assertHttpStatus(response, 400)
        self.assertIn('manufacturer', response.data)

    def test_create_with_missing_required_field(self):
        url = self._get_list_url()
        data = {'manufacturer': self.manufacturer.pk}

        response = self.client.post(url, data, format='json')
        self.assertHttpStatus(response, 400)
        self.assertIn('license_name', response.data)


class LicenseAssignmentAPITestCase(PluginAPITestCase):
    """Test LicenseAssignment API endpoints."""

    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(name='Acme Corp', slug='acme-corp')
        cls.software_license = SoftwareLicense.objects.create(
            manufacturer=manufacturer,
            license_name='API License',
            license_sku='SKU-1',
        )
        cls.site_type = ContentType.objects.get_for_model(Site)
        cls.site_1 = Site.objects.create(name='Site 1', slug='site-1')
        cls.site_2 = Site.objects.create(name='Site 2', slug='site-2')

        LicenseAssignment.objects.create(
            software_license=cls.software_license,
            object_type=cls.site_type,
            object_id=cls.site_1.pk,
        )

    def setUp(self):
        super().setUp()
        self.list_url_name = 'plugins-api:netbox_contracts-api:licenseassignment-list'
        self.detail_url_name = 'plugins-api:netbox_contracts-api:licenseassignment-detail'

    def test_list_license_assignments(self):
        self.add_permissions('netbox_contracts.view_licenseassignment')

        url = self._get_list_url()
        response = self.client.get(url)

        self.assertHttpStatus(response, 200)
        self.assertEqual(response.data['count'], 1)

    def test_list_license_assignments_without_permission(self):
        url = self._get_list_url()

        with disable_warnings('django.request'):
            response = self.client.get(url)
            self.assertHttpStatus(response, 403)

    def test_get_license_assignment(self):
        self.add_permissions('netbox_contracts.view_licenseassignment')

        instance = LicenseAssignment.objects.first()
        url = self._get_detail_url(instance)
        response = self.client.get(url)

        self.assertHttpStatus(response, 200)
        self.assertEqual(response.data['id'], instance.pk)
        self.assertEqual(response.data['object_type'], 'dcim.site')
        self.assertEqual(response.data['object_id'], self.site_1.pk)

    def test_create_license_assignment(self):
        self.add_permissions('netbox_contracts.add_licenseassignment')

        url = self._get_list_url()
        data = {
            'software_license': self.software_license.pk,
            'object_type': 'dcim.site',
            'object_id': self.site_2.pk,
        }

        response = self.client.post(url, data, format='json')
        self.assertHttpStatus(response, 201)

        instance = LicenseAssignment.objects.get(pk=response.data['id'])
        self.assertEqual(instance.software_license, self.software_license)
        self.assertEqual(instance.object_type, self.site_type)
        self.assertEqual(instance.object_id, self.site_2.pk)

    def test_create_license_assignment_without_permission(self):
        url = self._get_list_url()

        with disable_warnings('django.request'):
            response = self.client.post(url, {'object_type': 'dcim.site'}, format='json')
            self.assertHttpStatus(response, 403)

    def test_delete_license_assignment(self):
        self.add_permissions('netbox_contracts.delete_licenseassignment')

        instance = LicenseAssignment.objects.first()
        url = self._get_detail_url(instance)

        response = self.client.delete(url)
        self.assertHttpStatus(response, 204)

        self.assertFalse(LicenseAssignment.objects.filter(pk=instance.pk).exists())


class LicenseAssignmentAPIValidationTestCase(PluginAPITestCase):
    """Test LicenseAssignment API validation."""

    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(name='Acme Corp', slug='acme-corp')
        cls.software_license = SoftwareLicense.objects.create(
            manufacturer=manufacturer,
            license_name='API License',
            license_sku='SKU-1',
        )

    def setUp(self):
        super().setUp()
        self.add_permissions('netbox_contracts.add_licenseassignment')
        self.list_url_name = 'plugins-api:netbox_contracts-api:licenseassignment-list'

    def test_create_with_missing_software_license(self):
        url = self._get_list_url()
        data = {'object_type': 'dcim.site', 'object_id': 1}

        response = self.client.post(url, data, format='json')
        self.assertHttpStatus(response, 400)
        self.assertIn('software_license', response.data)

    def test_create_with_invalid_object_type(self):
        url = self._get_list_url()
        data = {
            'software_license': self.software_license.pk,
            'object_type': 'not.real',
            'object_id': 1,
        }

        response = self.client.post(url, data, format='json')
        self.assertHttpStatus(response, 400)
        self.assertIn('object_type', response.data)
