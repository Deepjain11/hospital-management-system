from django.test import override_settings
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from accounts.models import Doctor, Patient
from .models import Appointment

User = get_user_model()

@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}})
class coreManagementTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username='admin', password='password', role='admin', is_staff=True)
        
        self.doc_user = User.objects.create_user(username='doctor1', password='password', role='doctor')
        self.doctor = Doctor.objects.create(user=self.doc_user, specialty='Cardiology')
        
        self.pat_user = User.objects.create_user(username='patient1', password='password', role='patient')
        self.patient = Patient.objects.create(user=self.pat_user, date_of_birth='1990-01-01')
        
        self.appointment = Appointment.objects.create(
            doctor=self.doctor,
            patient=self.patient,
            date='2025-05-05',
            time='10:00:00',
            status='scheduled'
        )

    def test_unauthenticated_access(self):
        response = self.client.get('/api/core/appointments/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patient_can_view_own_appointment(self):
        self.client.force_authenticate(user=self.pat_user)
        response = self.client.get('/api/core/appointments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_admin_can_view_all_appointments(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get('/api/core/appointments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_dashboard_stats_admin_only(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get('/api/core/dashboard-stats/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.client.force_authenticate(user=self.pat_user)
        response = self.client.get('/api/core/dashboard-stats/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
