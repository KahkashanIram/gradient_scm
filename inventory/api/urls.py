from django.urls import path
from inventory.api.views.available_stock import AvailableStockAPIView
from inventory.api.views.expired_stock import ExpiredStockAPIView
from inventory.api.views.movement import InventoryMovementAPIView



urlpatterns = [
    path("inventory/available/", AvailableStockAPIView.as_view()),
    path("inventory/expired/", ExpiredStockAPIView.as_view()),
    path("inventory/movements/", InventoryMovementAPIView.as_view()),
]

