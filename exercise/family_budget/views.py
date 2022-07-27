from rest_framework import viewsets
from .models import Budget
from .serializers import BudgetSerializer


class BudgetAPIViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
