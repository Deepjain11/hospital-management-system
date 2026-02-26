from rest_framework import serializers
from .models import Invoice
from core.serializers import AppointmentSerializer

class InvoiceSerializer(serializers.ModelSerializer):
    appointment_details = AppointmentSerializer(source='appointment', read_only=True)

    class Meta:
        model = Invoice
        fields = '__all__'
