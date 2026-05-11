from django.db.models import Q
from django.utils.translation import gettext_lazy as _

ASSIGNMENT_TYPES = (
    'circuits.circuit',
    'circuits.virtualcircuit',
    'dcim.site',
    'dcim.device',
    'dcim.rack',
    'virtualization.virtualmachine',
    'virtualization.cluster',
    'ipam.ipaddress',
    'ipam.prefix',
)

def build_models_q(model_strings):
    """Build a Q object from a list of 'app_label.model' strings."""
    q = Q()
    for model_string in model_strings:
        app_label, model = model_string.split('.')
        q |= Q(app_label=app_label, model=model)
    return q

ASSIGNMENT_MODELS = build_models_q(ASSIGNMENT_TYPES)