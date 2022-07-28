from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"budgets", views.BudgetAPIViewSet, basename="budgets")
router.register(r"incomes", views.IncomeAPIViewSet, basename="incomes")
router.register(r"expenses", views.ExpenseAPIViewSet, basename="expenses")

urlpatterns = [
    path("", include(router.urls)),
    path("register/", views.UserCreateAPIView.as_view(), name="register"),
]
