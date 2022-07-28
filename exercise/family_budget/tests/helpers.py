from decimal import Decimal

from rest_framework.request import Request

from family_budget.serializers import ExpenseSerializer, IncomeSerializer


def create_budgets_for_user(user, budget, income, expense):
    user_owner = user()

    budget_1 = budget(owner=user_owner)
    income(budget=budget_1)
    expense(budget=budget_1)
    budget_2 = budget(owner=user_owner)
    return user_owner, budget_1, budget_2


def authenticate_client(client, user):
    client.force_authenticate(user=user)
    return client


def compare_budgets(budget_result, budget_input, request):
    """
    Compare budgets data.
    Incomes and expenses comparisons had to use requests because of the HyperlinkedIdentityField inside them
    """
    assert budget_result["name"] == budget_input.name
    assert (
        budget_result["incomes"]
        == IncomeSerializer(
            budget_input.incomes.all(), many=True, context={"request": Request(request)}
        ).data
    )
    assert (
        budget_result["expenses"]
        == ExpenseSerializer(
            budget_input.expenses.all(),
            many=True,
            context={"request": Request(request)},
        ).data
    )


def compare_incomes_expenses(model, create_data, budget):
    """
    Compare incomes or expenses data.
    """
    assert model.objects.first().budget == budget
    assert model.objects.first().amount == Decimal(create_data["amount"])
    assert model.objects.first().category == create_data["category"]
