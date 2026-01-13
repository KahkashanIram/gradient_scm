from django import forms
from apps.sales.models.sales_order import SalesOrder


class SalesOrderCreateForm(forms.ModelForm):
    """
    Phase D0 — Sales Order Capture Form

    Purpose:
    - Manual sales order entry
    - No business logic
    - No inventory or planning logic
    - Pure data capture only
    """

    class Meta:
        model = SalesOrder
        fields = [
            "customer_name",
            "product_title",
            "product_id",
            "product_description",
            "is_new_product",
            "quantity",
            "requested_date",
            "expected_delivery_date",
        ]

        widgets = {
            "customer_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Customer Name",
                }
            ),
            "product_title": forms.TextInput(
            attrs={
            "class": "form-control",
            "placeholder": "Product title (e.g. Industrial Silicone Resin)",
                }
            ),
            "product_id": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Product ID (if known)",
                }
            ),
            "product_description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Product description / specifications",
                }
            ),
            "is_new_product": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "quantity": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1,
                }
            ),
            "requested_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),
            "expected_delivery_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),
        }

    def clean_quantity(self):
        """
        Ensure quantity is always positive.
        """
        quantity = self.cleaned_data.get("quantity")
        if quantity is None or quantity <= 0:
            raise forms.ValidationError("Quantity must be greater than zero.")
        return quantity

    def clean(self):
        """
        Basic cross-field validation:
        - Expected delivery date should not be before requested date
        """
        cleaned_data = super().clean()
        requested_date = cleaned_data.get("requested_date")
        expected_delivery_date = cleaned_data.get("expected_delivery_date")

        if (
            requested_date
            and expected_delivery_date
            and expected_delivery_date < requested_date
        ):
            raise forms.ValidationError(
                "Expected delivery date cannot be earlier than requested date."
            )

        return cleaned_data
