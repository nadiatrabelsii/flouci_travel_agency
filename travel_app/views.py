from rest_framework import viewsets
from django.contrib.auth.models import User
from .models import Package, Booking
from .serializers import UserSerializer, PackageSerializer, BookingSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from .tasks import send_booking_confirmation_email, generate_pdf_invoice

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class PackageViewSet(viewsets.ModelViewSet):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        """
        Custom action to confirm a booking, triggers email and PDF tasks.
        """
        booking = self.get_object()
        booking.status = 'confirmed'
        booking.save()

        # Trigger Celery tasks
        send_booking_confirmation_email.delay(
            to_email=booking.user.email,
            booking_details=str(booking.id)
        )
        generate_pdf_invoice.delay(booking.id)

        return Response({'status': 'Booking confirmed, tasks scheduled.'})
