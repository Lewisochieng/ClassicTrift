
from django.contrib import admin
from django.urls import path
from ClassicApp import views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('collection/', views.collection, name='collection'),
    path('contact/', views.contacts, name='contact'),
    path('base/', views.base, name='base'),
    path('categories/', views.categories, name='categories'),
    path('register/', views.register, name='register'),
    path('', views.login, name='login'),
    path('details/<int:product_id>/', views.details, name='details'),
    path('cart/', views.view_cart, name='cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:cart_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.stk, name='checkout'),
    path('success/', views.success, name='success'),

    path('pay/', views.pay, name='pay'),
    path('stk/', views.stk, name='stk'),
    path('token/', views.token, name='token')


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)