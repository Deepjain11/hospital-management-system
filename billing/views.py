from rest_framework import viewsets, permissions
from .models import Invoice
from .serializers import InvoiceSerializer

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Invoice.objects.select_related('appointment__doctor__user', 'appointment__patient__user')
        if user.role == 'admin':
            return queryset
        elif user.role == 'doctor':
            return queryset.filter(appointment__doctor__user=user)
        elif user.role == 'patient':
            return queryset.filter(appointment__patient__user=user)
        return Invoice.objects.none()
