from django.urls import path
from . import views
# from .charts import *
# from . import export

#class based views
from .views import ForeasListView,ForeasListViewVisibleFalse,EpafiListView
# from .delete_records import AithmaDeleteView,ForeasDeleteView,ContactDeleteView,ErgasiaDeleteView,AdeiaDeleteView,ServiceDeleteView,SellCornfirmDelete,TrainingDeleteView,HardwareDeleteView
# from .search import HomePageSearchListView
# from .update_records import AdeiaUpdateView

urlpatterns = [

    path('acs-services/foreas', ForeasListView.as_view(), name='pelatis'),
    path('acs-services/foreas-in-active', ForeasListViewVisibleFalse.as_view(), name='in_active_pelatis'),
    path('acs-services/edit/<int:dhmos_id>/',views.edit_forea, name='edit_forea'),
    path('acs-services/delete/<int:pk>/', views.soft_delete_dhmos, name='soft_delete_dhmos'),
    path('acs-services/restore/<int:pk>/', views.restore_dhmos, name='restore_dhmos'),
    path('acs-services/contacts/', EpafiListView.as_view(), name='contact'),
    path('acs-services/edit/contact/<int:employee_id>/',views.edit_contact, name='edit_contact'),
#     path('acs-services/update/contact/<int:pk>/',views.epafi_update, name='epafi_update'),
#     path('acs-services/carrier/tasks', ErgasiesListView.as_view(), name='ergasia'),
#     path('acs-services/update/task/<int:pk>/',views.ergasia_update, name='ergasia_update'),
#     path('acs-services/update/new_task/<int:pk>/',views.ergasia_copy_paste, name='ergasia_copy_paste'),
#     path('acs-services/carrier/days-off', AdeiaListView.as_view(), name='adeia'),
#     path('acs-services/update/days-off/<int:pk>/',AdeiaUpdateView.as_view(), name='adeia_update'),
#     path('acs-services/carrier/requests', AithmataListView.as_view(), name='aithma'),
#     path('acs-services/update/request/<int:pk>/',views.aithma_update, name='aithma_update'),
#     path('acs-services/carrier/sales', PolisiListView.as_view(), name='polisi'),
#     path('acs-services/update/sales/<int:pk>/',views.polisi_update, name='polisi_update'),
#     path('acs-services/carrier/service', ServiceListView.as_view(), name='service'),
#     path('acs-services/update/service/<int:pk>/',views.service_update, name='service_update'),
#     path('acs-services/carrier/hardware', HardwareListView.as_view(), name='hardware'),
#     path('acs-services/update/hardware/<int:pk>/',views.hardware_update, name='hardware_update'),
#     path('acs-services/carrier/training', TrainingListVew.as_view(), name='training'),
#     path('acs-services/update/training/<int:pk>/',views.training_update, name='training_update'),
#     path('acs-services/carrier/software', SoftwareListView.as_view(), name='software'),
#     path('password_reset', views.password_reset_request, name="password_reset"),
#     #search
#     path('acs-services/search/tasks-search',ErgasiesSearchListView.as_view(), name='ergasia_search'),
#     path('acs-services/search/sales-search',SalesSearchListView.as_view(), name='polisi_search'),
#     path('acs-services/search/day-off-search', DayOffSearchListView.as_view(), name='dayoff_search'),
#     #add new records
#     path('acs-services/new/client',views.dhmospost_new, name='pelatis_new'),
#     path('acs-services/new/contact',views.epafi_new, name='epafi_new'),
#     path('acs-services/new/task',views.ergasia_new, name='ergasia_new'),
#     path('acs-services/new/day-off',views.adeia_new, name='adeia_new'),
#     path('acs-services/new/request',views.aithma_new, name='aithma_new'),
#     path('acs-services/new/sale',views.polisi_new, name='polisi_new'),
#     path('acs-services/new/service',views.service_new, name='service_new'),
#     path('acs-services/new/training',views.training_new, name='training_new'),
#     path('acs-services/new/hardware',views.hardware_new, name='hardware_new'),
#     # delete records
#     path('delete-pelatis/<int:pk>/',ForeasDeleteView.as_view(), name='delete_pelatis'),
#     path('delete-epafi/<int:pk>/', ContactDeleteView.as_view(), name='delete_epafi'),
#     path('delete-ergasia/<int:pk>/',ErgasiaDeleteView.as_view(), name='delete_ergasia'),
#     path('delete_adeia/<int:pk>/', AdeiaDeleteView.as_view(), name='delete_adeia'),
#     path('delete_aithma/<int:pk>/', AithmaDeleteView.as_view(), name='delete_aithma'),
#     path('delete_polisi/<int:pk>/', SellCornfirmDelete.as_view(), name='delete_polisi'),
#     path('delete_service/<int:pk>/',ServiceDeleteView.as_view(), name='delete_service'),
#     path('delete_training/<int:pk>/',TrainingDeleteView.as_view(), name='delete_training'),
#     path('delete_hardware/<int:pk>/',HardwareDeleteView.as_view(), name='delete_hardware'),
#     # chained selection ergasia_new
#     path('api/ergasies/dhmoi-epafes/<int:pk>/', views.api_dhmos, name='api_dhmos'),
#     path('api/ergasies-update/dhmoi-epafes/<int:pk>/', views.api_dhmos_update, name='api_dhmos_update'),
#     path('api/aithmata/dhmoi-epafes/<int:pk>/', views.api_aithma, name='api_aithma'),
#     # path(r'api/prosfora/dhmoi-epafes/<int:pk>/', timologisi.views.api_dhmos_prosfora, name='api_dhmos_prosfora'),
#     # charts
#     path('acs-services/day-off-charts', AdeiaChartView.as_view(), name='adeia_chart'),
#     path('acs-services/sales-chart', PolisiChartView.as_view(), name='polisi_chart'),
#     path('acs-services/task-chart', ErgasiaChartView.as_view(), name='ergasia_chart'),
#     # export csv,xls
#     path('acs-services/export-employees-xls/', views.export_epafes, name='export'),
#     path('acs-services/export-employees-csv/csv', views.employees_csv_export, name='export_csv'),
#     path('acs-services/export-ergasies/', views.export_ergasies, name='export_ergasies'),
#     path('acs-services/export-ergasies-all/', views.export_ergasies_all, name='export_ergasies_all'),
#     path('acs-services/export-adeies-all/', views.export_adeies_all, name='export_adeies_all'),
#     path('acs-services/search_items/', search_items, name='search_items'),
 ]