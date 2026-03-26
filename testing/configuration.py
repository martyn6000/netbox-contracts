###################################################################
#  This file serves as a base configuration for testing purposes  #
#  only. It is not intended for production use.                   #
###################################################################

ALLOWED_HOSTS = ["*"]

DATABASE = {
    "NAME": "netbox",
    "USER": "netbox",
    "PASSWORD": "netbox",
    "HOST": "localhost",
    "PORT": "",
    "CONN_MAX_AGE": 300,
}

FIELD_CHOICES = {
    'netbox_contracts.Contract.internal_party': (
        ('default', 'Default entity', 'green'),
        ('entity1', 'Entity 1', 'green'),
        ('entity2', 'Entity 2', 'yellow'),
    ),
    'netbox_contracts.Contract.currency': (
        ('usd', 'USD'),
        ('eur', 'EUR'),
        ('chf', 'CHF'),
        ('pln', 'PLN'),
    ),
    'netbox_contracts.Contract.status': (
        ('active', 'Active', 'green'),
        ('canceled', 'Canceled', 'red'),
    ),
}

PLUGINS = [
    'netbox_contracts',
]

PLUGINS_CONFIG = {
    'netbox_contracts': {
        'top_level_menu': True,
        'mandatory_contract_fields': [],
        'hidden_contract_fields': [],
        'mandatory_invoice_fields': [],
        'hidden_invoice_fields': [],
    }
}

REDIS = {
    "tasks": {
        "HOST": "localhost",
        "PORT": 6379,
        "PASSWORD": "",
        "DATABASE": 0,
        "SSL": False,
    },
    "caching": {
        "HOST": "localhost",
        "PORT": 6379,
        "PASSWORD": "",
        "DATABASE": 1,
        "SSL": False,
    },
}

SECRET_KEY = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
