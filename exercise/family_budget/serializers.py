from rest_framework import serializers
from .models import Budget


class BudgetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    incomes = serializers.HyperlinkedIdentityField(view_name='incomes', format='html', many=True)
    expenses = serializers.HyperlinkedIdentityField(view_name='expenses', format='html', many=True)

    class Meta:
        model = Budget
        fields = [
            'id',
            'name',
            'owner',
            'incomes',
            'expenses',
        ]
