from rest_framework import serializers
from .models import Package, Booking
from rest_framework.serializers import Serializer, CharField

class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

class LoginSerializer(Serializer):
    username = CharField()
    password = CharField(write_only=True)
