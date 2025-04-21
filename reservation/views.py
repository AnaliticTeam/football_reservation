from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Payment, Reservation, Stadium , ApiUrls
from .serializers import ApiUrlsSerializer, PaymentSerializer, ReservationSerializer, StadiumSerializer
from django.views.decorators.csrf import csrf_exempt # for skip token


@csrf_exempt
@api_view(['GET'])
def api_urls(request):
    api_urls = ApiUrls.objects.all()
    serializer = ApiUrlsSerializer(api_urls, many=True)
    return Response(serializer.data)




# Get the list of stadiums (GET request) and Create a new stadium (POST request)
@csrf_exempt
@api_view(['GET', 'POST'])
def stadium_list(request):
    if request.method == 'GET':
        stadiums = Stadium.objects.all()
        serializer = StadiumSerializer(stadiums, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        # Ensure that the data passed is valid for creating a new stadium
        serializer = StadiumSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Save the new stadium instance
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Get, Update, or Delete a specific stadium (GET, PUT, DELETE requests)
@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def stadium_detail(request, pk):
    try:
        stadium = Stadium.objects.get(pk=pk)
    except Stadium.DoesNotExist:
        return Response({"detail": "Stadium not found."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # Fetch a specific stadium by ID
        serializer = StadiumSerializer(stadium)
        return Response(serializer.data)

    elif request.method == 'PUT':
        # Update the stadium
        serializer = StadiumSerializer(stadium, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # Delete the stadium
        stadium.delete()
        return Response({"detail": "Stadium deleted successfully."}, status=status.HTTP_204_NO_CONTENT)






@api_view(['POST', 'GET'])
def create_reservation(request):
    if request.method == 'POST':
        serializer = ReservationSerializer(data=request.data)
        if serializer.is_valid():
            # Ensure that the user who is making the reservation is set (assuming they are logged in)
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # If the serializer is not valid, return the error details
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        # This could be a separate logic if you want to retrieve reservations (you may want a list of all reservations)
        reservations = Reservation.objects.all()
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data)

@api_view(['GET', 'PUT', 'DELETE'])
def reservation_detail(request, pk):
    try:
        reservation = Reservation.objects.get(pk=pk)
    except Reservation.DoesNotExist:
        return Response({"detail": "Reservation not found."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # Fetch a specific reservation by ID
        serializer = ReservationSerializer(reservation)
        return Response(serializer.data)

    elif request.method == 'PUT':
        # Update the reservation
        serializer = ReservationSerializer(reservation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # Delete the reservation
        reservation.delete()
        return Response({"detail": "Reservation deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def create_payment(request, reservation_id):
    try:
        reservation = Reservation.objects.get(id=reservation_id)
    except Reservation.DoesNotExist:
        return Response({"detail": "Reservation not found."}, status=status.HTTP_404_NOT_FOUND)

    if reservation.paid:
        return Response({"detail": "This reservation has already been paid for."}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'POST':
        # Assuming you are handling the payment logic here, such as connecting to a payment gateway
        payment_data = {
            'reservation': reservation.id,
            'amount': reservation.total_price,
            'payment_method': request.data.get('payment_method', 'Unknown'),
            'payment_status': 'Completed',  # Or 'Pending', depending on the payment gateway status
        }
        payment_serializer = PaymentSerializer(data=payment_data)
        if payment_serializer.is_valid():
            payment_serializer.save()
            # Mark the reservation as paid
            reservation.paid = True
            reservation.save()
            return Response(payment_serializer.data, status=status.HTTP_201_CREATED)
        return Response(payment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def payment_detail(request, pk):
    try:
        payment = Payment.objects.get(pk=pk)
    except Payment.DoesNotExist:
        return Response({"detail": "Payment not found."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # Fetch a specific payment by ID
        serializer = PaymentSerializer(payment)
        return Response(serializer.data)

    elif request.method == 'PUT':
        # Update the payment
        serializer = PaymentSerializer(payment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # Delete the payment
        payment.delete()
        return Response({"detail": "Payment deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
