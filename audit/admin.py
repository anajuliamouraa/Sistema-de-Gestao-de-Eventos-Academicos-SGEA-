from django.contrib import admin
from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'user', 'action', 'object_type', 'object_repr', 'ip_address']
    list_filter = ['action', 'timestamp', 'object_type']
    search_fields = ['user__username', 'description', 'object_repr', 'ip_address']
    readonly_fields = ['user', 'action', 'description', 'ip_address', 'user_agent', 
                       'object_type', 'object_id', 'object_repr', 'extra_data', 'timestamp']
    date_hierarchy = 'timestamp'
    ordering = ['-timestamp']
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
