from django.contrib import admin
from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('allauth.urls')),


    #  <<----- main urls ----->>
    path('',views.home,name='home'),
    path('cofe_home/',views.cofe_home,name='cofe_home'),
    path('cake_education/',views.cake_education,name='cake_education'),
    path('academy/',views.academy,name='academy'),
    path('cofee_delivery/',views.cofee_delivery,name='cofee_delivery'),

     #  <<----- cart urls ----->>
    path('cart/add/<int:academy_product_id>/<int:coffee_delivery_id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:academy_product_id>/<int:coffee_delivery_id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/',views.cart_detail,name='cart_detail'),


     #  <<----- dashboard urls ----->>
     path('dashboard/',views.dashboard,name='dashboard'),
     path('add_to_favorite/<str:item_type>/<int:item_id>/', views.add_to_favorite, name='add_to_favorite'),
     path('remove_from_favorite/<str:item_type>/<int:item_id>/', views.remove_from_favorite, name='remove_from_favorite'),
     path('change_password/', views.change_password, name='change_password'),


    #  <<----- sale main urls ----->>
    path('courses/<int:course_id>/',views.courses,name='courses'),
    path('coffee_delivery_sale/<int:coffee_delivery_sale_id>/',views.coffee_delivery_sale,name='coffee_delivery_sale'),
    path('academy_sale/<int:academy_sale_id>/',views.academy_sale,name='academy_sale'),


    # <<----- login-register-logout-contacts ---->>
    path('login_register/',views.login_register,name='login_register'),
    path('logout/',views.custom_logout,name='custom_logout'),
    path('register/',views.register,name='register'),
    path("contact/",views.contact,name="contact"),
    path("second_contact/",views.second_contact,name="second_contact"),




     # <<----- EMIAL PASSWORD ----->>
    path('reset_password/', auth_views.PasswordResetView.as_view
         (template_name='main/reset_password.html')
         ,name='reset_password'),


    path('reset-password_sent/', auth_views.PasswordResetDoneView.as_view
         (template_name='main/password_reset_sent.html')
         ,name='password_reset_done'),


    path('reset-password_complete/', auth_views.PasswordResetCompleteView.as_view
         (template_name='main/change_password_done.html')
         ,name='password_reset_complete'),


    path('reset/uidb64/<token>',auth_views.PasswordResetConfirmView.as_view
          (template_name='main/change_password_done.html')
         ,name='password_reset_confirm'),



     # <<----- Payment ----->>
     path('index/', views.index, name='index'),
     # path('odeme/<int:course_id>/', views.odeme, name='odeme'),
     # path('ok-url/', views.ok_url,name='ok_url'),
     # path('fail-url/', views.fail_url,name='fail_url'),


     path('purchase_course/<int:course_id>/', views.purchase_course, name='purchase_course'),

     path('payment_confirmation/<int:course_id>/', views.payment_confirmation, name='payment_confirmation'),
     path('payment_failed/', views.payment_failed, name='payment_failed'),



     path('choose_product/', views.choose_product, name='choose_product'),
     


]


urlpatterns += static(settings.STATIC_URL , document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL , document_root=settings.MEDIA_ROOT)