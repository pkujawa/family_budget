from django.db import models
from django.utils.translation import gettext_lazy as _


class CategoryChoices(models.TextChoices):
    HOUSING = "HOUSING", _("Housing")
    TRANSPORTATION = "TRANSPORTATION", _("Transportation")
    FOOD = "FOOD", _("Food")
    MEDICAL_AND_HEALTHCARE = "MEDICAL_AND_HEALTHCARE", _("Medical & Healthcare")
    UTILITIES = "UTILITIES", _("Utilities")
    SAVING_AND_DEBT_PAYMENTS = "SAVING_AND_DEBT_PAYMENTS", _("Saving & Debt Payments")
    INSURANCE = "INSURANCE", _("Insurance")
    WORK = "WORK", _("Work")
    OTHER = "OTHER", _("Other")
