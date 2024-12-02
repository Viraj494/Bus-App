from django.contrib.auth import views as auth_views
from django.urls import path
from . import api
from . import views

# Updated app_name to make it unique
app_name = 'creator_app'

urlpatterns = [
    
    path('create-payment/', views.create_payment, name='create_payment'),
    path('webhook/', views.webhook, name='webhook'),

    path('childCreate/', views.children_form, name="children_insert"),
    path('childList/', views.children_list, name="children_list"),
    path('childUpdate<int:id>/', views.children_form, name="children_update"),
    path('childDelete/<int:id>', views.children_delete, name="children_delete"),
    
    path('adultsCreate/', views.adults_form, name="adults_insert"),
    path('adultsList/', views.adults_list, name="adults_list"),
    path('<int:id>/', views.adults_form, name="adults_update"),
    path('adultsDelete/<int:id>', views.adults_delete, name="adults_delete"),
    
    path('adultsCardCreate/', views.adultsCard_form, name="adultsCard_insert"),
    path('adultCardList/', views.adultsCard_list, name="adultsCard_list"),
    path('adultCardUpdate/<int:id>/', views.adultsCard_form, name="adultsCard_update"),
    path('adultCardDelete/<int:id>', views.adultsCard_delete, name="adultsCard_delete"),
    
    path('childCardCreate/', views.childrenCard_form, name="childrenCard_insert"),
    path('childCardList/', views.childrCard_list, name="childCard_list"),
    path('childCardUpdate/<int:id>/', views.childrenCard_form, name="childrenCard_update"),
    path('childCardDelete/<int:id>', views.childrenCard_delete, name="childrenCard_delete"),
    
    
    path('combined_data/', views.combined_data_view, name='combined_data'),
     
    # Passenger URLs
    path('create/', views.passenger_form, name="passenger_insert"),
    path('list/', views.passenger_list, name="passenger_list"),
    path('passengerUpdate/<int:id>/', views.passenger_form, name="passenger_update"),
    path('delete/<int:id>', views.passenger_delete, name="passenger_delete"),
    
    # Registered Passenger URLs
    path('createReg/', views.combined_form, name="combined_insert"),
    path('listReg/', views.combined_list, name="combined_list"),
    path('reg/<int:id>/', views.combined_form, name="combined_update"),
    path('deleteReg/<int:id>', views.combined_delete, name="combined_delete"),
    
    # Admin Registered Passenger URLs
    path('admin/createReg/', views.admin_passenger_form, name="admin_reg_passenger_insert"),
    path('admin/listReg/', views.admin_passenger_list, name="admin_passenger_list"),
    path('admin/<int:id>/', views.admin_passenger_form, name="admin_reg_passenger_update"),
    path('admin/deleteReg/<int:id>', views.admin_passenger_delete, name="admin_reg_passenger_delete"),
    
    path('passengerHome/', views.passenger_home, name="passenger_home"),
    path('selectCat/', views.select_cat, name="select_cat"),
    path('adminHome/', views.admin_home, name="admin_home"),
    path('managePassengers/', views.manage_passengers, name="manage_passengers"),
]
