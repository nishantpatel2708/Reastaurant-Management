from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'rest_admin'

urlpatterns = [

    path('qr/', views.qr, name='qr'),
    path('add_menu/', views.add_menu, name='add_menu'),
    path('add_employee/', views.add_employee, name='add_employee'),
    path('add_category/', views.add_categories, name='add_category'),
    path('cat_list/', views.category_list, name='cat_list'),
    path('menu_list/', views.menu_list, name='menu_list'),
    path('menu_state/<int:id>/', views.menu_avc, name='menu_state'),
    path('emp_list/', views.employee_list, name='emp_list'),
    path('edit_cat/<int:id>/', views.cat_form_edit, name='edit_cat'),
    path('delete_cat/<int:id>/', views.delete, name='delete_cat'),
    path('edit_emp/<int:id>/', views.emp_form_edit, name='edit_emp'),
    path('delete_emp/<int:id>/', views.emp_delete, name='delete_emp'),
    path('edit_menu/<int:id>/', views.menu_form_edit, name='edit_menu'),
    path('delete_menu/<int:id>/', views.menu_delete, name='delete_menu'),
    path('t_earn/', views.t_price, name='t_price'),

    path('orders/', views.orders, name='orders'),
    path('t_orders/', views.today_order, name='t_order'),
    path('orders_det/<int:id>/', views.order_details, name='order_det'),
    path('complete/<int:id>/', views.order_complete, name='order_complete'),
    path('pdf/<int:id>/', views.GeneratePdf.as_view(), name='pdf'),
    path('menu_state/<int:id>/', views.menu_avc, name='menu_state'),
    path('user_profile/', views.user_details, name='user_profile'),
    path('update_u/<int:id>/', views.update_details, name='update_u'),

    path('table_view/', views.table_view, name='table_view'),
    path('edit_table/<int:id>/', views.table_edit, name='edit_table'),
    path('delete_table/<int:id>/', views.table_delete, name='delete_table'),

    path('table_list/', views.table_list, name='table_list'),
    path('report/', views.report, name='report'),
    path('com_u/<int:id>/', views.com_edit, name='com_u'),

    path('add_manager/', views.add_manager, name='add_manager'),
    path('manager_list/', views.manager_list, name='manager_list'),
    path('manager_form_edit/<int:id>/',
         views.manager_form_edit, name='manager_form_edit'),
    path('manager_delete/<int:id>/', views.manager_delete, name='manager_delete'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)