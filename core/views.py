from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.cache import cache
from .models import Appointment, Prescription
from .serializers import AppointmentSerializer, PrescriptionSerializer
from billing.models import Invoice

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Appointment.objects.select_related('doctor__user', 'patient__user')
        if user.role == 'admin':
            return queryset
        elif user.role == 'doctor':
            return queryset.filter(doctor__user=user)
        elif user.role == 'patient':
            return queryset.filter(patient__user=user)
        return Appointment.objects.none()

    def perform_create(self, serializer):
        appointment = serializer.save()
        Invoice.objects.create(appointment=appointment, amount=500.00)

class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Prescription.objects.select_related('appointment__doctor__user', 'appointment__patient__user')
        if user.role == 'admin':
            return queryset
        elif user.role == 'doctor':
            return queryset.filter(appointment__doctor__user=user)
        elif user.role == 'patient':
            return queryset.filter(appointment__patient__user=user)
        return Prescription.objects.none()

class DashboardStatsView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        stats = cache.get('dashboard_stats')
        if not stats:
            stats = {
                'total_appointments': Appointment.objects.count(),
                'total_prescriptions': Prescription.objects.count(),
                'total_invoices': Invoice.objects.count(),
            }
            cache.set('dashboard_stats', stats, 60 * 15)
        return Response(stats)
