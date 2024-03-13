from django.contrib import admin
from .models import Goal

@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('name', 'total_goal', 'amount_earned', 'amount_remaining', 'target_date')
    fields = ('account', 'name', 'total_goal', 'amount_earned', 'amount_remaining', 'target_date')
    readonly_fields = ('amount_remaining',)