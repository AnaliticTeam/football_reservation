from rest_framework import serializers
from .models import Stadium, Reservation, Payment,ApiUrls
from django.contrib.auth.models import User

class StadiumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stadium
        fields = ['id', 'name', 'location', 'owner', 'price']

class ReservationSerializer(serializers.ModelSerializer):
    stadium = StadiumSerializer(read_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())  # Link to user model
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Reservation
        fields = ['id', 'stadium', 'user', 'start_time', 'end_time', 'total_price', 'paid']

class PaymentSerializer(serializers.ModelSerializer):
    reservation = ReservationSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'reservation', 'amount', 'payment_date', 'payment_method', 'payment_status']  # Change 'status' to 'payment_status'


class ApiUrlsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApiUrls
        fields =['url']  # Include all fields or specify the ones you need
