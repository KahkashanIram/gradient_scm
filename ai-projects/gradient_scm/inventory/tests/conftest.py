import os
import django
import pytest
from rest_framework.test import APIClient

# Force Django setup for pytest
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()


@pytest.fixture
def api_client():
    return APIClient()
