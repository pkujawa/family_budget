from django.contrib import admin
from django.urls import include, path
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title="Budgets API")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("family_budget.urls")),
    path("api/", schema_view),
]

urlpatterns += [
    path("api-auth/", include("rest_framework.urls")),
]
