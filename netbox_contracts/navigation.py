from django.conf import settings
from django.utils.translation import gettext_lazy as _
from netbox.plugins import PluginMenu, PluginMenuButton, PluginMenuItem

plugin_settings = settings.PLUGINS_CONFIG['netbox_contracts']

contract_buttons = [
    PluginMenuButton(
        link='plugins:netbox_contract:contract_add',
        title=_('Add'),
        icon_class='mdi mdi-plus-thick',
        permissions=['netbox_contract.add_contract'],
    )
]

contracttype_buttons = [
    PluginMenuButton(
        link='plugins:netbox_contract:contracttype_add',
        title=_('Add'),
        icon_class='mdi mdi-plus-thick',
        permissions=['netbox_contract.add_contract'],
    )
]

provider_buttons = [
    PluginMenuButton(
        link='plugins:netbox_contract:provider_add',
        title=_('Add'),
        icon_class='mdi mdi-plus-thick',
        permissions=['netbox_contract.add_provider'],
    )
]

servicelevelagreement_buttons = [
    PluginMenuButton(
        link='plugins:netbox_contract:servicelevelagreement_add',
        title=_('Add'),
        icon_class='mdi mdi-plus-thick',
        permissions=['netbox_contract.add_servicelevelagreement'],
    )
]

provideraccount_buttons = [
    PluginMenuButton(
        link='plugins:netbox_contract:provideraccount_add',
        title=_('Add'),
        icon_class='mdi mdi-plus-thick',
        permissions=['netbox_contract.add_provideraccount'],
    )
]

contract_menu_item = PluginMenuItem(
    link='plugins:netbox_contract:contract_list',
    link_text=_('Contracts'),
    buttons=contract_buttons,
    permissions=['netbox_contract.view_contract'],
)

contracttype_menu_item = PluginMenuItem(
    link='plugins:netbox_contract:contracttype_list',
    link_text=_('Contract type'),
    buttons=contracttype_buttons,
    permissions=['netbox_contract.view_contract'],
)

provider_menu_item = PluginMenuItem(
    link='plugins:netbox_contract:provider_list',
    link_text=_('Providers'),
    buttons=provider_buttons,
    permissions=['netbox_contract.view_provider'],
)

provideraccount_menu_item = PluginMenuItem(
    link='plugins:netbox_contract:provideraccount_list',
    link_text=_('Provider Accounts'),
    buttons=provideraccount_buttons,
    permissions=['netbox_contract.view_provideraccount'],
)

contract_assignemnt_menu_item = PluginMenuItem(
    link='plugins:netbox_contract:contractassignment_list',
    link_text=_('Contracts assignments'),
    permissions=['netbox_contract.view_contractassignment'],
)

servicelevelagreement_menu_item = PluginMenuItem(
    link='plugins:netbox_contract:servicelevelagreement_list',
    link_text=_('Service Level Agreement'),
    buttons=contract_buttons,
    permissions=['netbox_contract.view_servicelevelagreement'],
)

items = (
    contract_menu_item,
    contracttype_menu_item,
    provider_menu_item,
    provideraccount_menu_item,
    servicelevelagreement_menu_item,
    contract_assignemnt_menu_item,
)

if plugin_settings.get('top_level_menu'):
    menu = PluginMenu(
        label=_('Contracts'),
        groups=(('Contracts', items),),
        icon_class='mdi mdi-file-sign',
    )
else:
    menu_items = items
