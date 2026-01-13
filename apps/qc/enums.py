from django.db import models

class QCRecipeStatus(models.TextChoices):
    DRAFT = "DRAFT", "Draft"
    VALIDATED = "VALIDATED", "Validated"
