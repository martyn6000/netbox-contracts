from django.urls import include, path
from netbox.views.generic import ObjectChangeLogView
from utilities.urls import get_model_urls

from . import models, views

urlpatterns = (
    # Providers
    path('providers/', include(get_model_urls('circuits', 'provider', detail=False))),
    path('providers/<int:pk>/', include(get_model_urls('circuits', 'provider'))),
    # Provider Accounts
    path('provider-accounts/', include(get_model_urls('circuits', 'provideraccount', detail=False))),
    path('provider-accounts/<int:pk>/', include(get_model_urls('circuits', 'provideraccount'))),

    # Contracts
    path('contracts/', views.ContractListView.as_view(), name='contract_list'),
    path('contracts/add/', views.ContractEditView.as_view(), name='contract_add'),
    path(
        'contracts/import/',
        views.ContractBulkImportView.as_view(),
        name='contract_bulk_import',
    ),
    path(
        'contracts/edit/',
        views.ContractBulkEditView.as_view(),
        name='contract_bulk_edit',
    ),
    path(
        'contracts/delete/',
        views.ContractBulkDeleteView.as_view(),
        name='contract_bulk_delete',
    ),
    path(
        'contracts/<int:pk>/',
        include(get_model_urls('netbox_contract', 'contract')),
        name='contract',
    ),
    path(
        'contracts/<int:pk>/edit/',
        views.ContractEditView.as_view(),
        name='contract_edit',
    ),
    path(
        'contracts/<int:pk>/delete/',
        views.ContractDeleteView.as_view(),
        name='contract_delete',
    ),
    path(
        'contracts/<int:pk>/changelog/',
        ObjectChangeLogView.as_view(),
        name='contract_changelog',
        kwargs={'model': models.Contract},
    ),
    # Service Level Agreements
    path('servicelevelagreement/', views.ServiceLevelAgreementListView.as_view(), name='servicelevelagreement_list'),
    path('servicelevelagreement/add/', views.ServiceLevelAgreementEditView.as_view(), name='servicelevelagreement_add'),
    path(
        'servicelevelagreement/import/', views.ServiceLevelAgreementBulkImportView.as_view(), name='servicelevelagreement_bulk_import'
    ),
    path(
        'servicelevelagreement/edit/', views.ServiceLevelAgreementBulkEditView.as_view(), name='servicelevelagreement_bulk_edit'
    ),
    path(
        'servicelevelagreement/delete/',
        views.ServiceLevelAgreementBulkDeleteView.as_view(),
        name='servicelevelagreement_bulk_delete',
    ),
    path(
        'servicelevelagreement/<int:pk>/',
        include(get_model_urls('netbox_contract', 'servicelevelagreement')),
        name='servicelevelagreement',
    ),
    path(
        'servicelevelagreement/<int:pk>/edit/', views.ServiceLevelAgreementEditView.as_view(), name='servicelevelagreement_edit'
    ),
    path(
        'servicelevelagreement/<int:pk>/delete/',
        views.ServiceLevelAgreementDeleteView.as_view(),
        name='servicelevelagreement_delete',
    ),
    path(
        'servicelevelagreement/<int:pk>/changelog/',
        ObjectChangeLogView.as_view(),
        name='servicelevelagreement_changelog',
        kwargs={'model': models.ServiceLevelAgreement},
    ),
    # Contract assignments
    path(
        'assignments/',
        views.ContractAssignmentListView.as_view(),
        name='contractassignment_list',
    ),
    path(
        'assignments/add/',
        views.ContractAssignmentEditView.as_view(),
        name='contractassignment_add',
    ),
    path(
        'assignments/import/',
        views.ContractAssignmentBulkImportView.as_view(),
        name='contractassignment_bulk_import',
    ),
    path(
        'assignments/edit/',
        views.ContractAssignmentBulkEditView.as_view(),
        name='contractassignment_bulk_edit',
    ),
    path(
        'assignments/delete/',
        views.ContractAssignmentBulkDeleteView.as_view(),
        name='contractassignment_bulk_delete',
    ),
    path(
        'assignments/<int:pk>/',
        views.ContractAssignmentView.as_view(),
        name='contractassignment',
    ),
    path(
        'assignments/<int:pk>/edit/',
        views.ContractAssignmentEditView.as_view(),
        name='contractassignment_edit',
    ),
    path(
        'assignments/<int:pk>/delete/',
        views.ContractAssignmentDeleteView.as_view(),
        name='contractassignment_delete',
    ),
    path(
        'assignments/<int:pk>/changelog/',
        ObjectChangeLogView.as_view(),
        name='contractassignment_changelog',
        kwargs={'model': models.ContractAssignment},
    ),
    
)
