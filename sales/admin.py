from django.contrib import admin
from .models import Quote, QuoteLine

class QuoteLineInline(admin.TabularInline):
    model = QuoteLine
    extra = 0

@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ("number", "customer", "issue_date", "status", "total", "is_cancelled")
    search_fields = ("number", "customer__name")
    list_filter = ("status", "is_cancelled")
    inlines = [QuoteLineInline]
