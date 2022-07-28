from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import generics, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .models import Budget, Expense, Income
from .permissions import IsBudgetOwnerOrSharedWith, IsIncomeExpenseOwnerOrSharedWith
from .serializers import (
    BudgetCreateSerializer,
    BudgetSerializer,
    ExpenseCreateSerializer,
    ExpenseSerializer,
    IncomeCreateSerializer,
    IncomeSerializer,
    ShareBudgetSerializer,
    UserCreateSerializer,
)


class ListAllowedMixin:
    """
    Mixin class overriding `list` method so that the queryset is taken based on the allowed entries
    for the specific user
    """

    def allowed_queryset(self, request):
        raise NotImplemented

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.allowed_queryset(request))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class BudgetAPIViewSet(ListAllowedMixin, viewsets.ModelViewSet):
    queryset = Budget.objects.order_by("pk")
    serializer_class = BudgetSerializer
    permission_classes = [permissions.IsAuthenticated, IsBudgetOwnerOrSharedWith]

    def allowed_queryset(self, request):
        return self.get_queryset().filter(
            Q(owner=request.user) | Q(shared_with__in=[request.user])
        )

    def get_serializer_class(self):
        if self.action == "create":
            return BudgetCreateSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=["POST"])
    def share(self, request, *args, **kwargs):
        serializer = ShareBudgetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data["user"]
        user = get_object_or_404(User, username=username)

        budget = self.get_object()

        if request.user == budget.owner:
            budget.shared_with.add(user)
            return Response(status=status.HTTP_204_NO_CONTENT)

        raise PermissionDenied()


class IncomeAPIViewSet(ListAllowedMixin, viewsets.ModelViewSet):
    queryset = Income.objects.order_by("pk")
    serializer_class = IncomeSerializer
    permission_classes = [permissions.IsAuthenticated, IsIncomeExpenseOwnerOrSharedWith]
    filterset_fields = ("budget", "category")

    def allowed_queryset(self, request):
        return self.get_queryset().filter(
            Q(budget__owner=request.user) | Q(budget__shared_with__in=[request.user])
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "create":
            return IncomeCreateSerializer
        return self.serializer_class


class ExpenseAPIViewSet(ListAllowedMixin, viewsets.ModelViewSet):
    queryset = Expense.objects.order_by("pk")
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated, IsIncomeExpenseOwnerOrSharedWith]
    filterset_fields = ("budget", "category")

    def allowed_queryset(self, request):
        return self.get_queryset().filter(
            Q(budget__owner=request.user) | Q(budget__shared_with__in=[request.user])
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "create":
            return ExpenseCreateSerializer
        return self.serializer_class


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
