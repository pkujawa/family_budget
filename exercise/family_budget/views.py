from rest_framework import viewsets
from .models import Expense, Budget, Income
from .serializers import ExpenseSerializer, BudgetSerializer, IncomeSerializer


class BudgetAPIViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer


class IncomeAPIViewSet(viewsets.ModelViewSet):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer


class ExpenseAPIViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
