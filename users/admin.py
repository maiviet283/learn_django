from django.contrib import admin
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone_number', 'username', 'birth_date', 'created_at')
    list_filter = ('birth_date', 'created_at')
    search_fields = ('full_name', 'email', 'phone_number', 'username')
    ordering = ('-created_at',)
