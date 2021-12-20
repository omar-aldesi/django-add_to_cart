from django.conf.urls import url
from django.urls import path,include
from . import views 

  urlpatterns[
    path('add-to-cart/<str:slug>/',views.add_to_cart,name='add-to-cart'),
    path('remove-from-cart/<str:slug>/',views.remove_from_cart,name='remove-from-cart'),
    path('remove_from_cart_in_summary/<str:slug>/',views.remove_from_cart_in_summary,name='remove-from-cart-in-summary'),
    path('remove-item-from-cart/<str:slug>',views.remove_one_item_from_cart,name='remove-one-item-from-cart'),
    path('add_one_to_item_cart/<str:slug>',views.add_one_to_item_cart,name='add-one-item-to-cart'),
   ]
