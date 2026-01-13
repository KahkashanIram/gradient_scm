import pytest


@pytest.mark.django_db
def test_post_not_allowed_on_inventory_api(api_client):
    url = "/api/inventory/available/"
    response = api_client.post(url, {})

    assert response.status_code in (401, 403, 405)
