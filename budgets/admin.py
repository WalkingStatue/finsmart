from django.contrib import admin
from .models import Budget

class BudgetAdmin(admin.ModelAdmin):
    list_display = ('name', 'total_budget', 'amount_spent', 'amount_remaining', 'start_date', 'end_date', 'period')
    fields = ('account', 'name', 'total_budget', 'amount_spent', 'amount_remaining', 'start_date', 'end_date', 'period')
    # If you want to make 'amount_remaining' read-only:
    readonly_fields = ('amount_remaining',)

admin.site.register(Budget, BudgetAdmin)
