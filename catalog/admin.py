from django.contrib import admin
from .models import Service

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "unit", "unit_price", "tax_rate", "is_active")
    search_fields = ("name",)
    list_filter = ("is_active",)
