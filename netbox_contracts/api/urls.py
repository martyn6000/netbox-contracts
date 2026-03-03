from netbox.api.routers import NetBoxRouter

from . import views

app_name = 'netbox_contract'

router = NetBoxRouter()
router.register('contracts', views.ContractViewSet)
router.register('contracttype', views.ContractTypeViewSet)
router.register('contractassignment', views.ContractAssignmentViewSet)

urlpatterns = router.urls
