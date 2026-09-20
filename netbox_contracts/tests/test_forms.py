"""
Test cases for SCB Netbox contract plugin forms.
"""

from dcim.models import Manufacturer, Site
from django.contrib.contenttypes.models import ContentType
from ipam.models import VLAN

from ..forms import LicenseAssignmentForm
from ..models import LicenseAssignment, SoftwareLicense
from ..testing import PluginModelTestCase


class LicenseAssignmentFormTestCase(PluginModelTestCase):
    """Test the dynamic object_id lookup on LicenseAssignmentForm."""

    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(name='Acme Corp', slug='acme-corp')
        cls.software_license = SoftwareLicense.objects.create(
            manufacturer=manufacturer,
            license_name='Form License',
            license_sku='SKU-1',
        )
        cls.site_type = ContentType.objects.get_for_model(Site)
        cls.vlan_type = ContentType.objects.get_for_model(VLAN)
        cls.site = Site.objects.create(name='Site 1', slug='site-1')

    def test_object_id_disabled_without_object_type(self):
        form = LicenseAssignmentForm()
        self.assertTrue(form.fields['object_id'].disabled)

    def test_object_id_scoped_to_selected_object_type(self):
        form = LicenseAssignmentForm(data={'object_type': self.site_type.pk})
        self.assertFalse(form.fields['object_id'].disabled)
        self.assertEqual(form.fields['object_id'].queryset.model, Site)

    def test_object_id_queryset_changes_with_object_type(self):
        form = LicenseAssignmentForm(data={'object_type': self.vlan_type.pk})
        self.assertEqual(form.fields['object_id'].queryset.model, VLAN)

    def test_valid_submission_creates_assignment(self):
        form = LicenseAssignmentForm(
            data={
                'software_license': self.software_license.pk,
                'object_type': self.site_type.pk,
                'object_id': self.site.pk,
            }
        )

        self.assertTrue(form.is_valid(), form.errors)
        instance = form.save()

        self.assertEqual(instance.object_id, self.site.pk)
        self.assertEqual(instance.assigned_object, self.site)

    def test_object_id_must_match_selected_object_type(self):
        nonexistent_site_id = Site.objects.order_by('-pk').first().pk + 1000

        form = LicenseAssignmentForm(
            data={
                'software_license': self.software_license.pk,
                'object_type': self.site_type.pk,
                'object_id': nonexistent_site_id,
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn('object_id', form.errors)

    def test_edit_existing_assignment_prefills_object(self):
        assignment = LicenseAssignment.objects.create(
            software_license=self.software_license,
            object_type=self.site_type,
            object_id=self.site.pk,
        )

        form = LicenseAssignmentForm(instance=assignment)

        self.assertEqual(form.fields['object_id'].initial, self.site)


class SoftwareLicenseFormTestCase(PluginModelTestCase):
    """Test the local currency field on SoftwareLicenseForm."""

    def test_local_currency_field_present(self):
        from ..forms import SoftwareLicenseForm

        form = SoftwareLicenseForm()
        self.assertIn('local_currency', form.fields)
        self.assertFalse(form.fields['local_currency'].required)
