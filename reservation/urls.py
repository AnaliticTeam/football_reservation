from django.urls import path
from . import views

urlpatterns = [

    #ApiUrls
    path('apiurls/',views.api_urls,name='api-urls'),


    # Stadiums
    path('stadiums/', views.stadium_list, name='stadium-list'),
    
    # Reservations
    path('reservations/', views.create_reservation, name='create-reservation'),  # POST request to create reservation
    path('reservations/<int:pk>/', views.reservation_detail, name='reservation-detail'),  # GET, PUT, DELETE reservation by ID
    
    # Payments
    path('reservations/<int:reservation_id>/payment/', views.create_payment, name='create-payment'),  # POST payment for reservation
    path('payments/<int:pk>/', views.payment_detail, name='payment-detail'),  # GET, PUT, DELETE payment by ID
]
