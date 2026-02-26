from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Doctor, Patient

class CustomUserAdmin(UserAdmin):
    model = User
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('role', 'phone_number')}),
    )

admin.site.register(User, CustomUserAdmin)

class DoctorAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'specialty', 'experience_years', 'contact_number')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'specialty')

    def get_username(self, obj):
        return f"Dr. {obj.user.get_full_name() or obj.user.username}"
    get_username.short_description = 'Doctor'

class PatientAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'date_of_birth', 'address')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')

    def get_username(self, obj):
        return obj.user.get_full_name() or obj.user.username
    get_username.short_description = 'Patient'

admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Patient, PatientAdmin)
