from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .models import Expense, Budget, Income
from .serializers import BudgetSerializer, BudgetCreateSerializer, ExpenseCreateSerizalizer, ExpenseSerializer, IncomeCreateSerizalizer, IncomeSerializer, ShareBudgetSerializer
from django.contrib.auth.models import User
from .permissions import IsBudgetOwnerOrSharedWith, IsIncomeExpenseOwnerOrSharedWith
from django.db.models import Q


class ListAllowedMixin:
    """
    Mixin class overriding `list` method so that the queryset is taken based on the allowed entries
    for the specific user
    """
    def allowed_queryset(self, request):
        return self.get_queryset().filter(Q(owner=request.user) | Q(shared_with__in=[request.user]))

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.allowed_queryset(request))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class BudgetAPIViewSet(ListAllowedMixin, viewsets.ModelViewSet):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    permission_classes = [permissions.IsAuthenticated, IsBudgetOwnerOrSharedWith]

    def get_serializer_class(self):
        if self.action == "create":
            return BudgetCreateSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['POST'])
    def share(self, request, *args, **kwargs):
        serializer = ShareBudgetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['user']
        user = get_object_or_404(User, username=username)

        budget = self.get_object()
        budget.shared_with.add(user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class IncomeAPIViewSet(ListAllowedMixin, viewsets.ModelViewSet):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer
    permission_classes = [permissions.IsAuthenticated, IsIncomeExpenseOwnerOrSharedWith]
    filterset_fields = ('budget', 'category')

    def allowed_queryset(self, request):
        return self.get_queryset().filter(
            Q(budget__owner=request.user) | Q(budget__shared_with__in=[request.user])
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "create":
            return IncomeCreateSerizalizer
        return self.serializer_class


class ExpenseAPIViewSet(ListAllowedMixin, viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseCreateSerizalizer
    permission_classes = [permissions.IsAuthenticated, IsIncomeExpenseOwnerOrSharedWith]
    filterset_fields = ('budget', 'category')

    def allowed_queryset(self, request):
        return self.get_queryset().filter(
            Q(budget__owner=request.user) | Q(budget__shared_with__in=[request.user])
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "create":
            return ExpenseCreateSerizalizer
        return self.serializer_class
