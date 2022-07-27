from rest_framework import serializers
from .choices import CategoryChoices
from .models import Expense, Budget, Income
from django.contrib.auth.models import User


class IncomeExpenseSerizalizer(serializers.ModelSerializer):
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


class BudgetSerializer(serializers.HyperlinkedModelSerializer):
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
