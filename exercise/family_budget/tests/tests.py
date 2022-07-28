from decimal import Decimal

import pytest
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.reverse import reverse

from family_budget.models import Budget, Expense, Income
from family_budget.tests.helpers import (
    authenticate_client,
    compare_budgets,
    compare_incomes_expenses,
    create_budgets_for_user,
)

pytestmark = pytest.mark.django_db


def test_create_budget(client, user, create_budget_data):
    user_owner = user()
    client_owner = authenticate_client(client, user_owner)
    assert Budget.objects.count() == 0
    response = client_owner.post(
        reverse("budgets-list"), format="json", data=create_budget_data
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert Budget.objects.count() == 1
    budget_1 = Budget.objects.first()
    assert budget_1.name == create_budget_data["name"]
    assert Income.objects.first().budget == budget_1
    assert Expense.objects.first().budget == budget_1


def test_create_income(client, user, budget, create_income_data):
    user_owner = user()
    budget_1 = budget(owner=user_owner)
    client_owner = authenticate_client(client, user_owner)
    assert Income.objects.count() == 0
    response = client_owner.post(reverse("incomes-list"), data=create_income_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert Income.objects.count() == 1
    compare_incomes_expenses(Income, create_income_data, budget_1)


def test_create_expense(client, user, budget, create_expense_data):
    user_owner = user()
    budget_1 = budget(owner=user_owner)
    client_owner = authenticate_client(client, user_owner)
    assert Expense.objects.count() == 0
    response = client_owner.post(reverse("expenses-list"), data=create_expense_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert Expense.objects.count() == 1
    compare_incomes_expenses(Expense, create_expense_data, budget_1)


def test_list_budgets(client, user, budget, income, expense):

    user_owner, budget_1, budget_2 = create_budgets_for_user(
        user, budget, income, expense
    )

    client_owner = authenticate_client(client, user_owner)
    response = client_owner.get(reverse("budgets-list"))
    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 2
    compare_budgets(
        budget_result=response.data["results"][0],
        budget_input=budget_1,
        request=response.wsgi_request,
    )
    compare_budgets(
        budget_result=response.data["results"][1],
        budget_input=budget_2,
        request=response.wsgi_request,
    )


def test_list_budgets_unauthenticated(client, user, budget, income, expense):

    create_budgets_for_user(user, budget, income, expense)

    response = client.get(reverse("budgets-list"))
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_budget_sharing(client, user, budget, income, expense):

    user_owner, budget_1, budget_2 = create_budgets_for_user(
        user, budget, income, expense
    )
    user_to_share = user()

    # user should not see the budget if it was not shared with him -
    # while listing budgets
    client_unshared = authenticate_client(client, user_to_share)
    response_list = client_unshared.get(reverse("budgets-list"))
    assert response_list.status_code == status.HTTP_200_OK
    assert response_list.data["count"] == 0

    # user should not see the budget if it was not shared with him -
    # while retrieving specific budget
    response_get = client_unshared.get(
        reverse("budgets-detail", kwargs={"pk": budget_1.pk})
    )
    assert response_get.status_code == status.HTTP_403_FORBIDDEN

    # user should not see the income of the budget if the budget was not shared with him -
    # while listing incomes
    response_list_incomes = client_unshared.get(reverse("incomes-list"))
    assert response_list_incomes.status_code == status.HTTP_200_OK
    assert response_list_incomes.data["count"] == 0

    # user should not see the income of the budget if the budget was not shared with him -
    # while retrieving specific income
    response_get = client_unshared.get(
        reverse("incomes-detail", kwargs={"pk": budget_1.incomes.first().pk})
    )
    assert response_get.status_code == status.HTTP_403_FORBIDDEN

    # sharing the budget
    client_owner = authenticate_client(client, user_owner)
    client_owner.post(
        reverse("budgets-share", kwargs={"pk": budget_1.pk}),
        data={"user": user_to_share.username},
    )

    # user should see the budget if it was shared with him -
    # while listing budgets
    client_shared = authenticate_client(client, user_to_share)
    response_list = client_shared.get(reverse("budgets-list"))
    assert response_list.status_code == status.HTTP_200_OK
    assert response_list.data["count"] == 1
    compare_budgets(
        budget_result=response_list.data["results"][0],
        budget_input=budget_1,
        request=response_list.wsgi_request,
    )

    # user should see the budget if it was shared with him -
    # while retrieving specific budget
    response_get = client_shared.get(
        reverse("budgets-detail", kwargs={"pk": budget_1.pk})
    )
    assert response_get.status_code == status.HTTP_200_OK
    compare_budgets(
        budget_result=response_get.data,
        budget_input=budget_1,
        request=response_get.wsgi_request,
    )

    # user should see the income of the budget if the budget was shared with him -
    # while listing incomes
    response_list_incomes = client_unshared.get(reverse("incomes-list"))
    assert response_list_incomes.status_code == status.HTTP_200_OK
    assert response_list_incomes.data["count"] == 1

    # user should see the income of the budget if the budget was shared with him -
    # while retrieving specific income
    response_get_income = client_unshared.get(
        reverse("incomes-detail", kwargs={"pk": budget_1.incomes.first().pk})
    )
    assert response_get_income.status_code == status.HTTP_200_OK
    assert (
        Decimal(response_get_income.data["amount"]) == budget_1.incomes.first().amount
    )
    assert response_get_income.data["budget"] == str(budget_1)

    # user should not be able to share the budget that he does not own (that was shared with him)
    user_to_not_share = user()
    response_not_share = client_shared.post(
        reverse("budgets-share", kwargs={"pk": budget_1.pk}),
        data={"user": user_to_not_share.username},
    )
    assert response_not_share.status_code == status.HTTP_403_FORBIDDEN


def test_create_user(client, create_user_data):
    assert User.objects.count() == 0
    response = client.post(reverse("register"), data=create_user_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.count() == 1


def test_budget_model_revenue(budget, income, expense):
    budget_1 = budget()
    assert budget_1.revenue == 0
    income(amount=100, budget=budget_1)
    income(amount=10, budget=budget_1)
    expense(amount=1, budget=budget_1)
    assert budget_1.revenue == 109
