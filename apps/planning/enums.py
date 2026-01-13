from django.db import models

class PlanningStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    APPROVED = "APPROVED", "Approved"
    REJECTED = "REJECTED", "Rejected"
from django.db import models

class PurchaseRequisitionStatus(models.TextChoices):
    CREATED = "CREATED", "Created"
    RELEASED = "RELEASED", "Released"
    CLOSED = "CLOSED", "Closed"
