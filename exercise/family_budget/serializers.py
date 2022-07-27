from rest_framework import serializers
from .choices import CategoryChoices
from .models import Expense, Budget, Income
from django.contrib.auth.models import User
from rest_framework.exceptions import PermissionDenied


class IncomeExpenseSerizalizer(serializers.ModelSerializer):
    """
    Abstract serializer for incomes and expenses designed for listing and retrieving
    """
    category = serializers.CharField(source='get_category_display')
    budget = serializers.SerializerMethodField()

    class Meta:
        abstract = True
        fields = [
            'id',
            'amount',
            'category',
            'budget',
            'url',
        ]

    def get_budget(self, obj):
        return str(obj.budget)


class IncomeSerializer(IncomeExpenseSerizalizer):
    url = serializers.HyperlinkedIdentityField(view_name='incomes-detail', format='html')

    class Meta(IncomeExpenseSerizalizer.Meta):
        model = Income


class ExpenseSerializer(IncomeExpenseSerizalizer):
    url = serializers.HyperlinkedIdentityField(view_name='expenses-detail', format='html')

    class Meta(IncomeExpenseSerizalizer.Meta):
        model = Expense


class IncomeExpenseCreateSerizalizer(serializers.ModelSerializer):
    """
    Abstract serializer for creating incomes and expenses
    """
    class Meta:
        abstract = True
        fields = [
            'amount',
            'category',
            'budget',
        ]

    def create(self, validated_data):
        """
        Override `create` method to allow creating only incomes/expenses for budgets that the user
        has access to (is owner or the budget has been shared with him)
        """
        budget = validated_data['budget']
        user = validated_data.pop('user')
        if budget.owner == user or user in budget.shared_with.all():
            return super().create(validated_data)
        raise PermissionDenied()


class IncomeCreateSerizalizer(IncomeExpenseCreateSerizalizer):
    class Meta(IncomeExpenseCreateSerizalizer.Meta):
        model = Income


class ExpenseCreateSerizalizer(IncomeExpenseCreateSerizalizer):
    class Meta(IncomeExpenseCreateSerizalizer.Meta):
        model = Expense


class IncomeExpenseCreateBudgetSerizalizer(serializers.ModelSerializer):
    """
    Abstract serializer for incomes and expenses that are created as related objects during
    budget creation
    """
    class Meta:
        abstract = True
        fields = [
            'amount',
            'category',
        ]


class IncomeCreateBudgetSerizalizer(IncomeExpenseCreateBudgetSerizalizer):
    class Meta(IncomeExpenseCreateBudgetSerizalizer.Meta):
        model = Income


class ExpenseCreateBudgetSerizalizer(IncomeExpenseCreateBudgetSerizalizer):
    class Meta(IncomeExpenseCreateBudgetSerizalizer.Meta):
        model = Expense


class BudgetSerializer(serializers.HyperlinkedModelSerializer):
    """
    Budget serializer for listing and retrieving budgets
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    incomes = IncomeSerializer(many=True)
    expenses = ExpenseSerializer(many=True)

    class Meta:
        model = Budget
        fields = [
            'id',
            'name',
            'owner',
            'incomes',
            'expenses',
        ]


class BudgetCreateSerializer(serializers.HyperlinkedModelSerializer):
    """
    Budget serializer for creating budget objects with related incomes and expenses
    """
    incomes = IncomeCreateBudgetSerizalizer(many=True)
    expenses = ExpenseCreateBudgetSerizalizer(many=True)

    class Meta:
        model = Budget
        fields = [
            'name',
            'incomes',
            'expenses',
        ]

    def create(self, validated_data):
        """
        Override `create` method to allow creating incomes and expenses nested inside the budget
        """
        incomes = validated_data.pop('incomes')
        expenses = validated_data.pop('expenses')
        budget = super().create(validated_data)

        for income in incomes:
            income['budget'] = budget
            Income.objects.create(**income)

        for expense in expenses:
            expense['budget'] = budget
            Expense.objects.create(**expense)

        return budget


class ShareBudgetSerializer(serializers.Serializer):
    user = serializers.CharField()
