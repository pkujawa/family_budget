from django.db import models
from .choices import CategoryChoices


class IncomeExpense(models.Model):
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.CharField(choices=CategoryChoices.choices, default=CategoryChoices.OTHER, max_length=100)

    class Meta:
        abstract = True


class Income(IncomeExpense):
    budget = models.ForeignKey('Budget', related_name='incomes', on_delete=models.CASCADE)

    def __str__(self):
        return f'Income {self.id} from budget {self.budget.name}'


class Expense(IncomeExpense):
    budget = models.ForeignKey('Budget', related_name='expenses', on_delete=models.CASCADE)

    def __str__(self):
        return f'Expense {self.id} from budget {self.budget.name}'


class Budget(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey('auth.User', related_name='my_budgets', on_delete=models.CASCADE)
    shared_with = models.ManyToManyField('auth.User', related_name='shared_budgets', blank=True)

    def __str__(self):
        return f'{self.name} (id: {self.id})'
