from django.contrib import admin
from .models import Budget, Expense, Income


class IncomeInLine(admin.StackedInline):
    model = Income
    extra = 1


class ExpenseInLine(admin.StackedInline):
    model = Expense
    extra = 1


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    inlines = [IncomeInLine, ExpenseInLine]
    list_display = ('id', 'name', 'owner')
    list_filter = ['owner']
    search_fields = ['owner__username']


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'category')
    list_filter = ['category']


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'category')
    list_filter = ['category']
