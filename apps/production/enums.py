from django.db import models

class ProductionOrderStatus(models.TextChoices):
    CREATED = "CREATED", "Created"
    RELEASED = "RELEASED", "Released"
    COMPLETED = "COMPLETED", "Completed"
