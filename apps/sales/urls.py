from django.urls import path
from apps.sales import views

app_name = "sales"

urlpatterns = [
    # Phase D0 — Sales Order Capture
    path("create/", views.create_sales_order, name="order_create"),
    path("list/", views.sales_order_list, name="order_list"),
    path("detail/<uuid:order_id>/", views.sales_order_detail, name="order_detail"),
    path("submit/<uuid:order_id>/", views.submit_sales_order_view, name="order_submit"),
]
