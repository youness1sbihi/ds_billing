from django.contrib import admin
from .models import Invoice, InvoiceLine

class InvoiceLineInline(admin.TabularInline):
    model = InvoiceLine
    extra = 0

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("number", "customer", "issue_date", "status", "total", "is_cancelled")
    search_fields = ("number", "customer__name")
    list_filter = ("status", "is_cancelled")
    inlines = [InvoiceLineInline]
