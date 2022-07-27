from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .models import Expense, Budget, Income
from .serializers import ExpenseSerializer, BudgetSerializer, IncomeSerializer, ShareBudgetSerializer
from django.contrib.auth.models import User


class BudgetAPIViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer

    @action(detail=True, methods=['POST'])
    def share(self, request, *args, **kwargs):
        serializer = ShareBudgetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['user']
        user = get_object_or_404(User, username=username)

        budget = self.get_object()
        budget.shared_with.add(user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class IncomeAPIViewSet(viewsets.ModelViewSet):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer


class ExpenseAPIViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
