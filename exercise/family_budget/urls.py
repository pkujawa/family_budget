from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'budgets', views.BudgetAPIViewSet, basename='budgets')
router.register(r'incomes', views.IncomeAPIViewSet, basename='incomes')
router.register(r'expenses', views.ExpenseAPIViewSet, basename='expenses')

urlpatterns = [
    path('', include(router.urls)),
]
