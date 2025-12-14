from django.contrib import admin
from .models import Invoice, InvoiceLine
from .services import recompute_invoice_totals

class InvoiceLineInline(admin.TabularInline):
    model = InvoiceLine
    extra = 0

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("number", "customer", "issue_date", "status", "total", "is_cancelled")
    search_fields = ("number", "customer__name")
    list_filter = ("status", "is_cancelled")
    inlines = [InvoiceLineInline]

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        recompute_invoice_totals(form.instance)
