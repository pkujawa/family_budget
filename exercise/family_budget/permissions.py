from rest_framework import permissions


class IsBudgetOwnerOrSharedWith(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            request.user == obj.owner or
            request.user in obj.shared_with.all()
        )


class IsIncomeExpenseOwnerOrSharedWith(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            request.user == obj.budget.owner or
            request.user in obj.budget.shared_with.all()
        )
