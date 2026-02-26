from django.db import models
from core.models import Appointment

class Invoice(models.Model):
    STATUS_CHOICES = (
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled')
    )
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='invoice')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='unpaid')
    date_issued = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invoice for {self.appointment} - {self.amount} ({self.status})"
