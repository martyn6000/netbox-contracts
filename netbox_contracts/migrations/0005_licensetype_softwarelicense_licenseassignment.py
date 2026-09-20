import django.db.models.deletion
import taggit.managers
import utilities.fields
import utilities.json
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('dcim', '0207_remove_redundant_indexes'),
        ('extras', '0128_tableconfig'),
        ('netbox_contracts', '0004_currency_comments'),
    ]

    operations = [
        migrations.CreateModel(
            name='LicenseType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('custom_field_data', models.JSONField(blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.CharField(blank=True, max_length=200)),
                ('color', utilities.fields.ColorField(default='9e9e9e', max_length=6)),
                ('tags', taggit.managers.TaggableManager(through='extras.TaggedItem', to='extras.Tag')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='SoftwareLicense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('custom_field_data', models.JSONField(blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder)),
                ('license_name', models.CharField(max_length=150)),
                ('friendly_name', models.CharField(blank=True, max_length=150)),
                ('license_sku', models.CharField(max_length=100)),
                ('per_license_cost', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('license_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='software_licenses', to='netbox_contracts.licensetype')),
                ('local_currency', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='software_licenses', to='netbox_contracts.currency')),
                ('manufacturer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='software_licenses', to='dcim.manufacturer')),
                ('tags', taggit.managers.TaggableManager(through='extras.TaggedItem', to='extras.Tag')),
            ],
            options={
                'ordering': ('license_name',),
            },
        ),
        migrations.CreateModel(
            name='LicenseAssignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('custom_field_data', models.JSONField(blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder)),
                ('object_id', models.PositiveBigIntegerField()),
                ('object_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='contenttypes.contenttype')),
                ('software_license', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='assignments', to='netbox_contracts.softwarelicense')),
                ('tags', taggit.managers.TaggableManager(through='extras.TaggedItem', to='extras.Tag')),
            ],
            options={
                'ordering': ('software_license',),
                'indexes': [models.Index(fields=['object_type', 'object_id'], name='nbc_licassign_object_idx')],
                'constraints': [models.UniqueConstraint(fields=('software_license', 'object_type', 'object_id'), name='netbox_contracts_licenseassignment_unique_license_object')],
            },
        ),
    ]
