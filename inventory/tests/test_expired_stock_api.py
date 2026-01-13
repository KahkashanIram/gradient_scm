import pytest


@pytest.mark.django_db
def test_expired_stock_api_returns_200(api_client):
    url = "/api/inventory/expired/"
    response = api_client.get(url)

    assert response.status_code == 200
    assert "results" in response.data
