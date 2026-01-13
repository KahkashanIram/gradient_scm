import pytest
from django.urls import reverse
from inventory.models import InventoryBatch, InventoryItem


@pytest.mark.django_db
def test_available_stock_api_returns_200(api_client):
    url = "/api/inventory/available/"
    response = api_client.get(url)

    assert response.status_code == 200
    assert "results" in response.data
    assert "count" in response.data


@pytest.mark.django_db
def test_available_stock_filter_by_item(api_client):
    url = "/api/inventory/available/?item=RM-TEST-002"
    response = api_client.get(url)

    assert response.status_code == 200
    assert isinstance(response.data["results"], list)
