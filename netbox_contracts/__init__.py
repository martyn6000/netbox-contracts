from netbox.plugins import PluginConfig


class ContractsConfig(PluginConfig):
    name = 'netbox_contracts'
    verbose_name = 'SCB Netbox contract'
    description = 'SCB Contract management plugin for Netbox'
    version = '1.0'
    author = 'Martyn Stanton'
    author_email = 'marrtynstanton@hotmail.com'
    base_url = 'contracts'
    min_version = '4.3.0'
    required_settings = []
    default_settings = {
        'top_level_menu': True,
        'mandatory_contract_fields': [],
        'hidden_contract_fields': [],
        'mandatory_invoice_fields': [],
        'hidden_invoice_fields': [],
        'mandatory_dimensions': [],
        'supported_models': [
            'circuits.circuit',
            'circuits.virtualcircuit',
            'dcim.site',
            'dcim.device',
            'dcim.rack',
            'virtualization.virtualmachine',
            'virtualization.cluster',
        ],
    }


config = ContractsConfig
