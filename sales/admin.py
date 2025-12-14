from django.contrib import admin
from .models import Quote, QuoteLine
from .services import recompute_quote_totals

class QuoteLineInline(admin.TabularInline):
    model = QuoteLine
    extra = 0

@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ("number", "customer", "issue_date", "status", "total", "is_cancelled")
    search_fields = ("number", "customer__name")
    list_filter = ("status", "is_cancelled")
    inlines = [QuoteLineInline]

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        recompute_quote_totals(form.instance)
