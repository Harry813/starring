from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.admin_index_view, name='ADMIndex'),
    re_path(r'login/$', views.admin_login_view, name='ADMLogin'),
    path('logout/', views.admin_logout_view, name='ADMLogout'),
    path('articles/page<int:page>/', views.admin_article_index_view, name="ADMArticleIndex"),
    path('articles/create/', views.admin_article_create_view, name="ADMArticleCreate"),
    path('articles/article-<int:article_id>/', views.admin_article_edit_view, name="ADMArticleEdit"),
    path('customer/page<int:page>/', views.admin_customer_index_view, name="ADMCustomerIndex"),
    path('customer/profile-<str:customer_id>/', views.admin_customer_edit_view, name="ADMCustomerEdit"),
    path('customer/profile-<str:customer_id>/basic/', views.admin_customer_basic_edit_view,
         name="ADMCustomerBasicEdit"),
    path('customer/profile-<str:customer_id>/profile/', views.admin_customer_profile_edit_view,
         name="ADMCustomerProfileEdit"),
    path('staff/page<int:page>/', views.admin_staff_index_view, name="ADMStaffIndex"),
    path('staff/profile-<str:staff_id>/', views.admin_staff_edit_view, name="ADMStaffEdit"),
    path('staff/profile-<str:staff_id>/basic/', views.admin_staff_basic_edit_view, name="ADMStaffBasicEdit"),
    path('staff/profile-<str:staff_id>/profile/', views.admin_staff_profile_edit_view, name="ADMStaffProfileEdit"),
    path('staff/create/', views.admin_staff_create_view, name="ADMStaffCreate"),
    path('sector/', views.admin_news_sector_index_view, name="ADMNewsSectorIndex"),
    path('sector/<int:sid>/', views.admin_news_sector_edit_view, name="ADMNewsSectorEdit"),
    path('news/', views.admin_news_index_view, name="ADMNewsIndex"),
    path('news/create/', views.admin_news_create_view, name="ADMNewsCreate"),
    path('news/<int:nid>/', views.admin_news_edit_view, name="ADMNewsEdit"),
    # path('news/, views.admin_news_index_view', name="admin_news_edit_view"),
    path('slots/page<int:page>/', views.admin_slot_index_view, name="ADMSlotIndex"),
    path('navigator/', views.admin_navi_sector_index_view, name="ADMNaviSectorIndex"),
    path('navigator/delete/<int:secid>/', views.admin_navi_sector_delete, name="ADMNaviSectorDelete"),
    path('navigator/item/<int:secid>/', views.admin_navi_item_index_view, name="ADMNaviItemIndex"),
    path('navigator/item/<int:secid>/create/', views.admin_navi_item_create_view, name="ADMNaviItemCreate"),
    path('navigator/item/<int:secid>/edit/<int:itemid>/', views.admin_navi_item_edit_view, name="ADMNaviItemEdit"),
    path('navigator/item/<int:secid>/delete/<int:itemid>/', views.admin_navi_item_delete, name="ADMNaviItemDelete"),

    path('upload/image/article/', views.admin_article_image_upload, name="ADMImageUpload"),
]
