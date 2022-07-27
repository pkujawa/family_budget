import json
import os

from model_bakery import baker
import pytest
from rest_framework.test import APIClient
from pathlib import Path
from django.conf import settings


base_dir = settings.BASE_DIR / Path('family_budget/tests/resources')


@pytest.fixture()
def budget():
    def _budget(**kwargs):
        return baker.make("Budget", **kwargs)
    return _budget


@pytest.fixture()
def expense():
    def _expense(**kwargs):
        return baker.make("Expense", **kwargs)
    return _expense


@pytest.fixture()
def income():
    def _income(**kwargs):
        return baker.make("Income", **kwargs)
    return _income


@pytest.fixture()
def user():
    def _user(**kwargs):
        return baker.make("User", **kwargs)
    return _user


@pytest.fixture()
def client():
    client = APIClient()
    return client


@pytest.fixture()
def create_budget_data():
    with open(base_dir / 'create_budget.json') as file:
        yield json.load(file)


@pytest.fixture()
def create_income_data():
    with open(base_dir / 'create_income.json') as file:
        yield json.load(file)


@pytest.fixture()
def create_expense_data():
    with open(base_dir / 'create_expense.json') as file:
        yield json.load(file)

@pytest.fixture()
def create_user_data():
    with open(base_dir / 'create_user.json') as file:
        yield json.load(file)
