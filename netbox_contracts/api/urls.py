from netbox.api.routers import NetBoxRouter

from . import views

app_name = 'netbox_contracts'

router = NetBoxRouter()
router.register('contracts', views.ContractViewSet)
router.register('contract-types', views.ContractTypeViewSet)
router.register('contract-assignments', views.ContractAssignmentViewSet)
router.register('service-level-agreements', views.ServiceLevelAgreementViewSet)
router.register('currencies', views.CurrencyViewSet)
router.register('license-types', views.LicenseTypeViewSet)
router.register('software-licenses', views.SoftwareLicenseViewSet)
router.register('license-assignments', views.LicenseAssignmentViewSet)

urlpatterns = router.urls
