from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from .models import Budget, Expense, Income


class IncomeExpenseSerializer(serializers.ModelSerializer):
    """
    Abstract serializer for incomes and expenses designed for listing and retrieving
    """

    category = serializers.CharField(source="get_category_display")
    budget = serializers.SerializerMethodField()

    class Meta:
        abstract = True
        fields = [
            "id",
            "amount",
            "category",
            "budget",
            "url",
        ]

    def get_budget(self, obj):
        return str(obj.budget)


class IncomeSerializer(IncomeExpenseSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="incomes-detail", format="html"
    )

    class Meta(IncomeExpenseSerializer.Meta):
        model = Income


class ExpenseSerializer(IncomeExpenseSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="expenses-detail", format="html"
    )

    class Meta(IncomeExpenseSerializer.Meta):
        model = Expense


class IncomeExpenseCreateSerializer(serializers.ModelSerializer):
    """
    Abstract serializer for creating incomes and expenses
    """

    class Meta:
        abstract = True
        fields = [
            "amount",
            "category",
            "budget",
        ]

    def create(self, validated_data):
        """
        Override `create` method to allow creating only incomes/expenses for budgets that the user
        has access to (is owner or the budget has been shared with him)
        """
        budget = validated_data["budget"]
        user = validated_data.pop("user")
        if budget.owner == user or user in budget.shared_with.all():
            return super().create(validated_data)
        raise PermissionDenied()


class IncomeCreateSerializer(IncomeExpenseCreateSerializer):
    class Meta(IncomeExpenseCreateSerializer.Meta):
        model = Income


class ExpenseCreateSerializer(IncomeExpenseCreateSerializer):
    class Meta(IncomeExpenseCreateSerializer.Meta):
        model = Expense


class IncomeExpenseCreateBudgetSerializer(serializers.ModelSerializer):
    """
    Abstract serializer for incomes and expenses that are created as related objects during
    budget creation
    """

    class Meta:
        abstract = True
        fields = [
            "amount",
            "category",
        ]


class IncomeCreateBudgetSerializer(IncomeExpenseCreateBudgetSerializer):
    class Meta(IncomeExpenseCreateBudgetSerializer.Meta):
        model = Income


class ExpenseCreateBudgetSerializer(IncomeExpenseCreateBudgetSerializer):
    class Meta(IncomeExpenseCreateBudgetSerializer.Meta):
        model = Expense


class BudgetSerializer(serializers.ModelSerializer):
    """
    Budget serializer for listing and retrieving budgets
    """

    owner = serializers.ReadOnlyField(source="owner.username")
    incomes = IncomeSerializer(many=True)
    expenses = ExpenseSerializer(many=True)

    class Meta:
        model = Budget
        fields = [
            "id",
            "name",
            "owner",
            "revenue",
            "incomes",
            "expenses",
        ]


class BudgetCreateSerializer(serializers.ModelSerializer):
    """
    Budget serializer for creating budget objects with related incomes and expenses
    """

    incomes = IncomeCreateBudgetSerializer(many=True)
    expenses = ExpenseCreateBudgetSerializer(many=True)

    class Meta:
        model = Budget
        fields = [
            "name",
            "incomes",
            "expenses",
        ]

    def create(self, validated_data):
        """
        Override `create` method to allow creating incomes and expenses nested inside the budget
        """

        incomes = validated_data.pop("incomes")
        expenses = validated_data.pop("expenses")
        budget = super().create(validated_data)

        for income in incomes:
            income["budget"] = budget
            Income.objects.create(**income)

        for expense in expenses:
            expense["budget"] = budget
            Expense.objects.create(**expense)

        return budget


class ShareBudgetSerializer(serializers.Serializer):
    user = serializers.CharField()


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
        ]

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data.get("password"))
        return super().create(validated_data)
