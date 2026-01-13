from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from apps.sales.forms import SalesOrderCreateForm
from apps.sales.models.sales_order import SalesOrder
from apps.sales.services.sales_order_service import assign_order_code
from django.shortcuts import get_object_or_404
from apps.sales.services.sales_order_service import submit_sales_order
from apps.sales.enums import SalesOrderStatus

@login_required
def create_sales_order(request):
    """
    Phase D0 — Sales Order Capture (Same-page success flow)

    Responsibilities:
    - Create SalesOrder in DRAFT state
    - Assign system-generated order_code at creation time
    - Show success message
    - Redirect back to same page (PRG pattern)
    - DOES NOT trigger planning / R&D fan-out
    """

    if request.method == "POST":
        form = SalesOrderCreateForm(request.POST)

        if form.is_valid():
            order = form.save(commit=False)
            order.created_by = request.user.username
            order.save()

            # 🔑 Assign business order code (service-layer responsibility)
            assign_order_code(order)

            messages.success(
                request,
                "Sales order created successfully."
            )

            # Redirect back to same page:
            # - clears form
            # - prevents duplicate submit
            return redirect("sales:order_create")

    else:
        form = SalesOrderCreateForm()

    return render(
        request,
        "sales/order_create.html",
        {"form": form}
    )


@login_required
def sales_order_list(request):
    """
    Phase D1 — Sales Order List (Read-only table)

    Responsibilities:
    - Show all sales orders
    - Sorted by newest first
    - No edits / no deletes
    """

    orders = SalesOrder.objects.all().order_by("-created_at")

    return render(
        request,
        "sales/order_list.html",
        {"orders": orders}
    )


@login_required
def sales_order_detail(request, order_id):
    """
    Phase D2 — Sales Order Detail View (Read-only)

    Responsibilities:
    - Show complete order information
    - Expose planning mirror fields
    - No workflow mutation
    """

    order = SalesOrder.objects.get(id=order_id)

    return render(
        request,
        "sales/order_detail.html",
        {"order": order}
    )
@login_required
def submit_sales_order_view(request, order_id):
    """
    Phase D3 — Submit Sales Order to Planning

    - Allowed only for DRAFT orders
    - Locks the order
    - Triggers Planning & R&D fan-out
    """

    order = get_object_or_404(SalesOrder, id=order_id)

    if order.status != SalesOrderStatus.DRAFT:
        messages.error(
            request,
            "Only draft orders can be submitted to planning."
        )
        return redirect("sales:order_detail", order_id=order.id)

    try:
        submit_sales_order(order)
        messages.success(
            request,
            "Sales order submitted to planning successfully."
        )
    except Exception as exc:
        messages.error(
            request,
            f"Submission failed: {str(exc)}"
        )

    return redirect("sales:order_detail", order_id=order.id)