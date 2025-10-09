from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'patient', 'date', 'get_timeslot_display', 'status', 'created_at')
    list_filter = ('status', 'date', 'doctor', 'timeslot')
    search_fields = ('doctor__first_name', 'doctor__last_name', 'patient__first_name', 'patient__last_name')
    date_hierarchy = 'date'
    ordering = ('-date', '-timeslot')
    
    fieldsets = (
        ('Appointment Details', {
            'fields': ('doctor', 'patient', 'date', 'timeslot')
        }),
        ('Additional Information', {
            'fields': ('description', 'status')
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('doctor', 'patient')
    
    def has_change_permission(self, request, obj=None):
        return request.user.is_staff or request.user.role in ['admin', 'staff']
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.role == 'admin'
