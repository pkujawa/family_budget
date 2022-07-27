from django.db import models
from .choices import CategoryChoices


class IncomeExpense(models.Model):
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.CharField(choices=CategoryChoices.choices, default=CategoryChoices.OTHER, max_length=100)


class Income(IncomeExpense):
    budget = models.ForeignKey('Budget', related_name='incomes', on_delete=models.CASCADE)


class Expense(IncomeExpense):
    budget = models.ForeignKey('Budget', related_name='expenses', on_delete=models.CASCADE)


class Budget(models.Model):
    owner = models.ForeignKey('auth.User', related_name='my_budgets', on_delete=models.CASCADE)
    shared_with = models.ManyToManyField('auth.User', related_name='shared_budgets')
