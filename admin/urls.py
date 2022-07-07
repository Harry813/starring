from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.admin_index_view, name='ADMIndex'),
    re_path(r'login/$', views.admin_login_view, name='ADMLogin'),
    path('logout/', views.admin_logout_view, name='ADMLogout'),
    path('articles/page/<int:page>/', views.admin_article_index_view, name="ADMArticleIndex"),
    path('articles/create/', views.admin_article_create_view, name="ADMArticleCreate"),
    path('articles/edit/<int:article_id>/', views.admin_article_edit_view, name="ADMArticleEdit"),
    path('articles/delete/<int:article_id>/', views.admin_article_delete_view, name="ADMArticleDelete"),
    path('appointment/page/<int:page>/', views.admin_appointment_index_view, name="ADMAppointmentIndex"),
    path('appointment/edit/<str:aptid>/', views.admin_appointment_edit_view, name="ADMAppointmentEdit"),
    path('appointment/allocate/<str:aptid>/', views.admin_appointment_allocate_view, name="ADMAppointmentAllocate"),
    path('appointment/updates/<str:aptid>/', views.admin_appointment_updates_view, name="ADMAppointmentUpdates"),
    path('appointment/updates/create/<str:aptid>/', views.admin_appointment_update_create_view,
         name="ADMAppointmentUpdateCreate"),
    path('customer/page/<int:page>/', views.admin_customer_index_view, name="ADMCustomerIndex"),
    path('customer/profile-<str:customer_id>/', views.admin_customer_edit_view, name="ADMCustomerEdit"),
    path('customer/profile-<str:customer_id>/basic/', views.admin_customer_basic_edit_view,
         name="ADMCustomerBasicEdit"),
    path('customer/profile-<str:customer_id>/profile/', views.admin_customer_profile_edit_view,
         name="ADMCustomerProfileEdit"),
    path('staff/page/<int:page>/', views.admin_staff_index_view, name="ADMStaffIndex"),
    path('staff/profile/<str:staff_id>/', views.admin_staff_edit_view, name="ADMStaffEdit"),
    path('staff/profile/<str:staff_id>/basic/', views.admin_staff_basic_edit_view, name="ADMStaffBasicEdit"),
    path('staff/profile/<str:staff_id>/profile/', views.admin_staff_profile_edit_view, name="ADMStaffProfileEdit"),
    path('staff/create/', views.admin_staff_create_view, name="ADMStaffCreate"),
    path('newssector/', views.admin_news_sector_index_view, name="ADMNewsSectorIndex"),
    path('newssector/<int:sid>/', views.admin_news_sector_edit_view, name="ADMNewsSectorEdit"),
    path('newssector/<int:sid>/create/', views.admin_news_create_view, name="ADMNewsCreate"),
    path('newssector/<int:sid>/edit/<int:nid>/', views.admin_news_edit_view, name="ADMNewsEdit"),
    path('slots/page/<int:page>/', views.admin_slot_index_view, name="ADMSlotIndex"),
    path('slots/create/', views.admin_slot_create_view, name="ADMSlotCreate"),
    path('slots/edit/<str:sid>/', views.admin_slot_edit_view, name="ADMSlotEdit"),
    path('navigator/', views.admin_navi_sector_index_view, name="ADMNaviSectorIndex"),
    path('navigator/delete/<int:secid>/', views.admin_navi_sector_delete, name="ADMNaviSectorDelete"),
    path('navigator/item/<int:secid>/', views.admin_navi_item_index_view, name="ADMNaviItemIndex"),
    path('navigator/item/<int:secid>/create/', views.admin_navi_item_create_view, name="ADMNaviItemCreate"),
    path('navigator/item/<int:secid>/edit/<int:itemid>/', views.admin_navi_item_edit_view, name="ADMNaviItemEdit"),
    path('navigator/item/<int:secid>/delete/<int:itemid>/', views.admin_navi_item_delete, name="ADMNaviItemDelete"),
    path('sidebar/', views.admin_sidebar_index_view, name="ADMSidebarIndex"),
    path('sidebar/edit/<int:sdb_id>/', views.admin_sidebar_edit_view, name="ADMSidebarEdit"),
    path('indexList/sector/', views.admin_index_sector_index, name="ADMIndListSectorIndex"),
    path('indexList/sector/<int:secid>/', views.admin_index_sector_edit, name="ADMIndListSectorEdit"),
    path('indexList/sector/<int:secid>/create/', views.admin_index_item_create, name="ADMIndListItemCreate"),
    path('indexList/sector/<int:secid>/edit/<int:itemid>/', views.admin_index_item_edit, name="ADMIndListItemEdit"),
    path('indexList/sector/<int:secid>/delete/<int:itemid>/', views.admin_index_item_delete,
         name="ADMIndListItemDelete"),
    path('upload/image/article/', views.admin_article_image_upload, name="ADMImageUpload"),

    # Appointment Related Convenient Methods
    path('appointment/accept/<int:page>/<str:aptid>', views.admin_appointment_accept, name="ADMAppointmentAccept"),
    path('appointment/reject/<int:page>/<str:aptid>', views.admin_appointment_reject, name="ADMAppointmentReject"),
    path('appointment/success/<int:page>/<str:aptid>', views.admin_appointment_success, name="ADMAppointmentSuccess"),
    path('appointment/timeout/<int:page>/<str:aptid>', views.admin_appointment_timeout, name="ADMAppointmentTimeout"),
    path('appointment/paid/<int:page>/<str:aptid>', views.admin_appointment_paid, name="ADMAppointmentPaid")
]
