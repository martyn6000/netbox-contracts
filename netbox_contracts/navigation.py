from django.conf import settings
from django.utils.translation import gettext_lazy as _
from netbox.plugins import PluginMenu, PluginMenuButton, PluginMenuItem

plugin_settings = settings.PLUGINS_CONFIG['netbox_contracts']

contract_buttons = [
    PluginMenuButton(
        link='plugins:netbox_contracts:contract_add',
        title=_('Add'),
        icon_class='mdi mdi-plus-thick',
        permissions=['netbox_contracts.add_contract'],
    )
]

contracttype_buttons = [
    PluginMenuButton(
        link='plugins:netbox_contracts:contracttype_add',
        title=_('Add'),
        icon_class='mdi mdi-plus-thick',
        permissions=['netbox_contracts.add_contract'],
    )
]

provider_buttons = [
    PluginMenuButton(
        link='plugins:netbox_contracts:provider_add',
        title=_('Add'),
        icon_class='mdi mdi-plus-thick',
        permissions=['netbox_contracts.add_provider'],
    )
]

servicelevelagreement_buttons = [
    PluginMenuButton(
        link='plugins:netbox_contracts:servicelevelagreement_add',
        title=_('Add'),
        icon_class='mdi mdi-plus-thick',
        permissions=['netbox_contracts.add_servicelevelagreement'],
    )
]

provideraccount_buttons = [
    PluginMenuButton(
        link='plugins:netbox_contracts:provideraccount_add',
        title=_('Add'),
        icon_class='mdi mdi-plus-thick',
        permissions=['netbox_contracts.add_provideraccount'],
    )
]

contractassingmenttype_buttons = [
    PluginMenuButton(
        link='plugins:netbox_contracts:contractassignment_add',
        title=_('Add'),
        icon_class='mdi mdi-plus-thick',
        permissions=['netbox_contracts.add_contractassignment'],
    )
]

contract_menu_item = PluginMenuItem(
    link='plugins:netbox_contracts:contract_list',
    link_text=_('Contracts'),
    buttons=contract_buttons,
    permissions=['netbox_contracts.view_contract'],
)

contracttype_menu_item = PluginMenuItem(
    link='plugins:netbox_contracts:contracttype_list',
    link_text=_('Contract type'),
    buttons=contracttype_buttons,
    permissions=['netbox_contracts.view_contract'],
)

provider_menu_item = PluginMenuItem(
    link='plugins:netbox_contracts:provider_list',
    link_text=_('Providers'),
    buttons=provider_buttons,
    permissions=['netbox_contracts.view_provider'],
)

provideraccount_menu_item = PluginMenuItem(
    link='plugins:netbox_contracts:provideraccount_list',
    link_text=_('Provider Accounts'),
    buttons=provideraccount_buttons,
    permissions=['netbox_contracts.view_provideraccount'],
)

contract_assignemnt_menu_item = PluginMenuItem(
    link='plugins:netbox_contracts:contractassignment_list',
    link_text=_('Contracts assignments'),
    buttons=contractassingmenttype_buttons,
    permissions=['netbox_contracts.view_contractassignment'],
)

servicelevelagreement_menu_item = PluginMenuItem(
    link='plugins:netbox_contracts:servicelevelagreement_list',
    link_text=_('Service Level Agreement'),
    buttons=servicelevelagreement_buttons,
    permissions=['netbox_contracts.view_servicelevelagreement'],
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
