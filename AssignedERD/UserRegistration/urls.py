from django.urls import path, include
from . import views

app_name = 'UserRegistration'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name="register"),
    path('signin/', views.sign_in, name='sign_in'),
    path('my_account/', views.my_account, name='my_account'),
    path('my_bookings',views.my_bookings, name='my_bookings'),
    path('sign_out/', views.sign_out, name='sign_out'),
    path('destination/<int:destination_id>/', views.display_destination, name='destination'),
    path('my_wishlist/', views.display_wishlist, name='my_wishlist'),
    path('add_wishlist/', views.add_wishlist, name='add_wishlist'),
    path('add_book_order/', views.add_book_order, name='add_book_order'),
    path('manage_bookings/', views.manage_bookings, name='manage_bookings'),
    path('manage_destinations/', views.manage_destinations, name='manage_destinations'),
    path('manage_destinations/destination/<int:destination_id>/', views.edit_destination, name='edit_destination'),
    path('book_order/', views.book_order, name='book_order'),
]
