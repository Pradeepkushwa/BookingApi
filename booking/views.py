# booking/views.py

import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import FitnessClass, Booking
from .serializers import FitnessClassSerializer, BookingSerializer
from django.utils import timezone
from datetime import datetime
logger = logging.getLogger("booking")


class FitnessClassListView(APIView):
    def get(self, request):
        classes = FitnessClass.objects.filter(datetime__gte=datetime.now()).order_by('datetime')
        serializer = FitnessClassSerializer(classes, many=True)
        logger.info(f"Fetched {len(serializer.data)} upcoming classes.")
        return Response(serializer.data, status=status.HTTP_200_OK)


class BookClassView(APIView):
    def post(self, request):
        data = request.data
        class_id = data.get("class_id")
        name = data.get("client_name")
        email = data.get("client_email")

        if not all([class_id, name, email]):
            logger.error("Booking failed: Missing required fields.")
            return Response({"error": "Missing fields"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            fitness_class = FitnessClass.objects.get(id=class_id)
        except FitnessClass.DoesNotExist:
            logger.error(f"Booking failed: Class with id {class_id} not found.")
            return Response({"error": "Class not found"}, status=status.HTTP_404_NOT_FOUND)

        if fitness_class.available_slots < 1:
            logger.warning(f"Booking failed: No slots available for class {fitness_class.id}.")
            return Response({"error": "No slots available"}, status=status.HTTP_400_BAD_REQUEST)

        fitness_class.available_slots -= 1
        fitness_class.save()

        booking = Booking.objects.create(
            fitness_class=fitness_class,
            client_name=name,
            client_email=email
        )

        logger.info(f"Booking successful for class {fitness_class.id} by {email}.")
        return Response(BookingSerializer(booking).data, status=status.HTTP_201_CREATED)


class BookingListView(APIView):
    def get(self, request):
        email = request.query_params.get("email")
        if not email:
            logger.error("Bookings fetch failed: Email not provided.")
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        bookings = Booking.objects.filter(client_email=email)
        serializer = BookingSerializer(bookings, many=True)

        logger.info(f"Fetched {len(serializer.data)} bookings for email {email}.")
        return Response(serializer.data, status=status.HTTP_200_OK)
