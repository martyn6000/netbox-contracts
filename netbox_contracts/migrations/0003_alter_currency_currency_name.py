# Generated migration for increasing currency_name max_length

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netbox_contracts', '0002_alter_contract_contract_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currency',
            name='currency_name',
            field=models.CharField(max_length=100, verbose_name='currency name'),
        ),
    ]
