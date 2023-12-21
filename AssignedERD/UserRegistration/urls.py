from django.urls import path, include
from . import views

app_name = 'UserRegistration'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name="register"),
    path('signin/', views.sign_in, name='sign_in'),
    path('my_account/', views.my_account, name='my_account'),
    path('sign_out/', views.sign_out, name='sign_out'),
    path('destination/<int:destination_id>/', views.display_destination, name='destination'),
    path('my_wishlist/', views.display_wishlist, name='my_wishlist'),
    path('add_wishlist/', views.add_wishlist, name='add_wishlist'),
    path('manage_bookings/', views.manage_bookings, name='manage_bookings'),
    path('manage_destinations/', views.manage_destinations, name='manage_destinations'),
]
