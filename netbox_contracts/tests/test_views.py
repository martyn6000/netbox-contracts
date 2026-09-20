"""
Test cases for SCB Netbox contract plugin views.
"""

from dcim.models import Manufacturer, Site
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

from ..models import LicenseAssignment, LicenseType, SoftwareLicense
from ..testing import PluginViewTestCase
from ..testing.utils import disable_warnings, get_random_string


class LicenseTypeViewTestCase(PluginViewTestCase):
    """Test LicenseType views."""

    @classmethod
    def setUpTestData(cls):
        LicenseType.objects.create(name='View Type 1')
        LicenseType.objects.create(name='View Type 2')
        LicenseType.objects.create(name='View Type 3')

    def setUp(self):
        super().setUp()
        self.base_url = 'plugins:netbox_contracts:licensetype'

    def test_list_license_types(self):
        self.add_permissions('netbox_contracts.view_licensetype')

        url = reverse('plugins:netbox_contracts:licensetype_list')
        response = self.client.get(url)

        self.assertHttpStatus(response, 200)

    def test_list_license_types_without_permission(self):
        url = reverse('plugins:netbox_contracts:licensetype_list')

        with disable_warnings('django.request'):
            response = self.client.get(url)
            self.assertHttpStatus(response, 403)

    def test_view_license_type(self):
        self.add_permissions('netbox_contracts.view_licensetype')

        instance = LicenseType.objects.first()
        url = reverse('plugins:netbox_contracts:licensetype', kwargs={'pk': instance.pk})
        response = self.client.get(url)

        self.assertHttpStatus(response, 200)
        self.assertEqual(response.context['object'], instance)

    def test_create_license_type(self):
        self.add_permissions(
            'netbox_contracts.add_licensetype',
            'netbox_contracts.view_licensetype',
        )

        url = reverse('plugins:netbox_contracts:licensetype_add')
        name = f'Created {get_random_string(10)}'

        form_data = self.post_data(
            {
                'name': name,
                'color': '2196f3',
            }
        )

        response = self.client.post(url, form_data, follow=True)
        self.assertHttpStatus(response, 200)

        instance = LicenseType.objects.get(name=name)
        self.assertEqual(instance.name, name)

    def test_create_license_type_without_permission(self):
        url = reverse('plugins:netbox_contracts:licensetype_add')

        with disable_warnings('django.request'):
            response = self.client.get(url)
            self.assertHttpStatus(response, 403)

    def test_edit_license_type(self):
        self.add_permissions(
            'netbox_contracts.change_licensetype',
            'netbox_contracts.view_licensetype',
        )

        instance = LicenseType.objects.first()
        url = reverse('plugins:netbox_contracts:licensetype_edit', kwargs={'pk': instance.pk})

        new_name = f'Edited {get_random_string(10)}'
        form_data = self.post_data(
            {
                'name': new_name,
                'color': instance.color,
            }
        )

        response = self.client.post(url, form_data, follow=True)
        self.assertHttpStatus(response, 200)

        instance.refresh_from_db()
        self.assertEqual(instance.name, new_name)

    def test_delete_license_type(self):
        self.add_permissions(
            'netbox_contracts.delete_licensetype',
            'netbox_contracts.view_licensetype',
        )

        instance = LicenseType.objects.first()
        url = reverse('plugins:netbox_contracts:licensetype_delete', kwargs={'pk': instance.pk})

        response = self.client.post(url, {'confirm': True}, follow=True)
        self.assertHttpStatus(response, 200)

        self.assertFalse(LicenseType.objects.filter(pk=instance.pk).exists())

    def test_delete_license_type_without_permission(self):
        instance = LicenseType.objects.first()
        url = reverse('plugins:netbox_contracts:licensetype_delete', kwargs={'pk': instance.pk})

        with disable_warnings('django.request'):
            response = self.client.get(url)
            self.assertHttpStatus(response, 403)


class SoftwareLicenseViewTestCase(PluginViewTestCase):
    """Test SoftwareLicense views."""

    @classmethod
    def setUpTestData(cls):
        cls.manufacturer = Manufacturer.objects.create(name='Acme Corp', slug='acme-corp')
        cls.license_type = LicenseType.objects.create(name='Subscription')

        SoftwareLicense.objects.create(
            manufacturer=cls.manufacturer,
            license_name='View License 1',
            license_sku='SKU-1',
            license_type=cls.license_type,
        )
        SoftwareLicense.objects.create(
            manufacturer=cls.manufacturer,
            license_name='View License 2',
            license_sku='SKU-2',
        )

    def setUp(self):
        super().setUp()
        self.base_url = 'plugins:netbox_contracts:softwarelicense'

    def test_list_software_licenses(self):
        self.add_permissions('netbox_contracts.view_softwarelicense')

        url = reverse('plugins:netbox_contracts:softwarelicense_list')
        response = self.client.get(url)

        self.assertHttpStatus(response, 200)

    def test_list_software_licenses_without_permission(self):
        url = reverse('plugins:netbox_contracts:softwarelicense_list')

        with disable_warnings('django.request'):
            response = self.client.get(url)
            self.assertHttpStatus(response, 403)

    def test_view_software_license(self):
        self.add_permissions('netbox_contracts.view_softwarelicense')

        instance = SoftwareLicense.objects.first()
        url = reverse('plugins:netbox_contracts:softwarelicense', kwargs={'pk': instance.pk})
        response = self.client.get(url)

        self.assertHttpStatus(response, 200)
        self.assertEqual(response.context['object'], instance)

    def test_create_software_license(self):
        self.add_permissions(
            'netbox_contracts.add_softwarelicense',
            'netbox_contracts.view_softwarelicense',
        )

        url = reverse('plugins:netbox_contracts:softwarelicense_add')
        license_name = f'Created {get_random_string(10)}'

        form_data = self.post_data(
            {
                'manufacturer': self.manufacturer,
                'license_name': license_name,
                'license_sku': get_random_string(10),
                'per_license_cost': '9.99',
                'license_type': self.license_type,
            }
        )

        response = self.client.post(url, form_data, follow=True)
        self.assertHttpStatus(response, 200)

        instance = SoftwareLicense.objects.get(license_name=license_name)
        self.assertEqual(instance.license_name, license_name)

    def test_create_software_license_without_permission(self):
        url = reverse('plugins:netbox_contracts:softwarelicense_add')

        with disable_warnings('django.request'):
            response = self.client.get(url)
            self.assertHttpStatus(response, 403)

    def test_edit_software_license(self):
        self.add_permissions(
            'netbox_contracts.change_softwarelicense',
            'netbox_contracts.view_softwarelicense',
        )

        instance = SoftwareLicense.objects.first()
        url = reverse('plugins:netbox_contracts:softwarelicense_edit', kwargs={'pk': instance.pk})

        new_name = f'Edited {get_random_string(10)}'
        form_data = self.post_data(
            {
                'manufacturer': instance.manufacturer,
                'license_name': new_name,
                'license_sku': instance.license_sku,
            }
        )

        response = self.client.post(url, form_data, follow=True)
        self.assertHttpStatus(response, 200)

        instance.refresh_from_db()
        self.assertEqual(instance.license_name, new_name)

    def test_delete_software_license(self):
        self.add_permissions(
            'netbox_contracts.delete_softwarelicense',
            'netbox_contracts.view_softwarelicense',
        )

        instance = SoftwareLicense.objects.first()
        url = reverse('plugins:netbox_contracts:softwarelicense_delete', kwargs={'pk': instance.pk})

        response = self.client.post(url, {'confirm': True}, follow=True)
        self.assertHttpStatus(response, 200)

        self.assertFalse(SoftwareLicense.objects.filter(pk=instance.pk).exists())

    def test_delete_software_license_without_permission(self):
        instance = SoftwareLicense.objects.first()
        url = reverse('plugins:netbox_contracts:softwarelicense_delete', kwargs={'pk': instance.pk})

        with disable_warnings('django.request'):
            response = self.client.get(url)
            self.assertHttpStatus(response, 403)


class SoftwareLicenseFormTestCase(PluginViewTestCase):
    """Test SoftwareLicense form validation."""

    @classmethod
    def setUpTestData(cls):
        cls.manufacturer = Manufacturer.objects.create(name='Acme Corp', slug='acme-corp')

    def setUp(self):
        super().setUp()
        self.add_permissions(
            'netbox_contracts.add_softwarelicense',
            'netbox_contracts.view_softwarelicense',
        )

    def test_form_validation_missing_manufacturer(self):
        url = reverse('plugins:netbox_contracts:softwarelicense_add')
        form_data = self.post_data(
            {
                'license_name': 'Test',
                'license_sku': 'SKU-1',
            }
        )

        response = self.client.post(url, form_data)
        self.assertHttpStatus(response, 200)  # Form redisplay

        self.assertEqual(SoftwareLicense.objects.filter(license_name='Test').count(), 0)

    def test_form_validation_missing_required_fields(self):
        url = reverse('plugins:netbox_contracts:softwarelicense_add')
        form_data = self.post_data({'manufacturer': self.manufacturer})

        response = self.client.post(url, form_data)
        self.assertHttpStatus(response, 200)  # Form redisplay

        self.assertEqual(SoftwareLicense.objects.count(), 0)


class LicenseAssignmentViewTestCase(PluginViewTestCase):
    """Test LicenseAssignment views."""

    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(name='Acme Corp', slug='acme-corp')
        cls.software_license = SoftwareLicense.objects.create(
            manufacturer=manufacturer,
            license_name='View License',
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
        self.base_url = 'plugins:netbox_contracts:licenseassignment'

    def test_list_license_assignments(self):
        self.add_permissions('netbox_contracts.view_licenseassignment')

        url = reverse('plugins:netbox_contracts:licenseassignment_list')
        response = self.client.get(url)

        self.assertHttpStatus(response, 200)

    def test_list_license_assignments_without_permission(self):
        url = reverse('plugins:netbox_contracts:licenseassignment_list')

        with disable_warnings('django.request'):
            response = self.client.get(url)
            self.assertHttpStatus(response, 403)

    def test_view_license_assignment(self):
        self.add_permissions('netbox_contracts.view_licenseassignment')

        instance = LicenseAssignment.objects.first()
        url = reverse('plugins:netbox_contracts:licenseassignment', kwargs={'pk': instance.pk})
        response = self.client.get(url)

        self.assertHttpStatus(response, 200)
        self.assertEqual(response.context['object'], instance)

    def test_create_license_assignment(self):
        self.add_permissions(
            'netbox_contracts.add_licenseassignment',
            'netbox_contracts.view_licenseassignment',
        )

        url = reverse('plugins:netbox_contracts:licenseassignment_add')
        form_data = self.post_data(
            {
                'software_license': self.software_license,
                'object_type': self.site_type,
                'object_id': self.site_2.pk,
            }
        )

        response = self.client.post(url, form_data, follow=True)
        self.assertHttpStatus(response, 200)

        self.assertTrue(
            LicenseAssignment.objects.filter(
                software_license=self.software_license,
                object_type=self.site_type,
                object_id=self.site_2.pk,
            ).exists()
        )

    def test_create_license_assignment_without_permission(self):
        url = reverse('plugins:netbox_contracts:licenseassignment_add')

        with disable_warnings('django.request'):
            response = self.client.get(url)
            self.assertHttpStatus(response, 403)

    def test_delete_license_assignment(self):
        self.add_permissions(
            'netbox_contracts.delete_licenseassignment',
            'netbox_contracts.view_licenseassignment',
        )

        instance = LicenseAssignment.objects.first()
        url = reverse('plugins:netbox_contracts:licenseassignment_delete', kwargs={'pk': instance.pk})

        response = self.client.post(url, {'confirm': True}, follow=True)
        self.assertHttpStatus(response, 200)

        self.assertFalse(LicenseAssignment.objects.filter(pk=instance.pk).exists())

    def test_delete_license_assignment_without_permission(self):
        instance = LicenseAssignment.objects.first()
        url = reverse('plugins:netbox_contracts:licenseassignment_delete', kwargs={'pk': instance.pk})

        with disable_warnings('django.request'):
            response = self.client.get(url)
            self.assertHttpStatus(response, 403)


class SoftwareLicenseContractsTabTestCase(PluginViewTestCase):
    """Test the optional Contracts tab on the Software License page."""

    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(name='Acme Corp', slug='acme-corp')
        cls.software_license = SoftwareLicense.objects.create(
            manufacturer=manufacturer,
            license_name='Tab License',
            license_sku='SKU-1',
        )

    def test_tab_visible_with_no_assignments(self):
        self.add_permissions(
            'netbox_contracts.view_softwarelicense',
            'netbox_contracts.view_contractassignment',
        )

        detail_url = reverse('plugins:netbox_contracts:softwarelicense', kwargs={'pk': self.software_license.pk})
        tab_url = reverse('plugins:netbox_contracts:softwarelicense_contracts', kwargs={'pk': self.software_license.pk})

        response = self.client.get(detail_url)
        self.assertHttpStatus(response, 200)
        self.assertContains(response, tab_url)

    def test_contracts_tab_renders(self):
        self.add_permissions(
            'netbox_contracts.view_softwarelicense',
            'netbox_contracts.view_contractassignment',
        )

        url = reverse('plugins:netbox_contracts:softwarelicense_contracts', kwargs={'pk': self.software_license.pk})
        response = self.client.get(url)

        self.assertHttpStatus(response, 200)
