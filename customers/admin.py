from django.contrib import admin
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "ice", "phone", "email", "is_active")
    search_fields = ("name", "code", "ice")
    list_filter = ("is_active",)
