from django.db import models

class InventoryNature(models.TextChoices):
    RAW_MATERIAL = "RAW_MATERIAL", "Raw Material"
    PACKING_MATERIAL = "PACKING_MATERIAL", "Packing Material"
    WIP = "WIP", "Work In Progress"
    FINISHED_GOOD = "FINISHED_GOOD", "Finished Good"
    SCRAP = "SCRAP", "Scrap / Waste"
    MRO_SPARE = "MRO_SPARE", "Machine Spare (MRO)"
    STATIONERY = "STATIONERY", "Stationery / Consumable"


class InventoryUsage(models.TextChoices):
    TECHNICAL = "TECHNICAL", "Technical"
    OPERATIONAL = "OPERATIONAL", "Operational"
    BOTH = "BOTH", "Both"


class ProcurementType(models.TextChoices):
    PURCHASED = "PURCHASED", "Purchased"
    IN_HOUSE = "IN_HOUSE", "In-House"
    OUTSOURCED = "OUTSOURCED", "Outsourced"


class HazardClass(models.TextChoices):
    NON_HAZARDOUS = "NON_HAZARDOUS", "Non Hazardous"
    FLAMMABLE = "FLAMMABLE", "Flammable"
    CORROSIVE = "CORROSIVE", "Corrosive"
    TOXIC = "TOXIC", "Toxic"
    ENVIRONMENTALLY_SENSITIVE = "ENVIRONMENTALLY_SENSITIVE", "Environmentally Sensitive"


class ItemStatus(models.TextChoices):
    DRAFT = "DRAFT", "Draft"
    APPROVED = "APPROVED", "Approved"
    ACTIVE = "ACTIVE", "Active"
    DEPRECATED = "DEPRECATED", "Deprecated"
class QCStatus(models.TextChoices):
    QC_PENDING = "QC_PENDING", "QC Pending"
    QC_APPROVED = "QC_APPROVED", "QC Approved"
    QC_BLOCKED = "QC_BLOCKED", "QC Blocked"
    EXPIRED = "EXPIRED", "Expired"
