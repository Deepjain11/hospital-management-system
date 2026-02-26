from django.contrib import admin
from django.urls import path, include

admin.site.site_header = "City Hospital Management System"
admin.site.site_title = "City Hospital Admin Portal"
admin.site.index_title = "Welcome to City Hospital Administration"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/core/', include('core.urls')),
    path('api/billing/', include('billing.urls')),
]
