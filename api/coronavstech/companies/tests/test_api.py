import json
from unittest import TestCase
from django.test import Client
from django.urls import reverse
import pytest


class TestGetCompanies(TestCase):
    def test_zero_companies_should_return_empty_list(self) -> None:
        """Test that we GET zero companies. If we fetch the GET request we expect to get empty list."""
        client = Client()  # (1)
        # companies_url = "http://127.0.0.1:8000/companies/"
        companies_url = reverse("companies-list")  # (2)
        response = client.get(companies_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), [])  # (3)


if __name__ == '__main__':
    pytest.main()

"""
Notes:
(1) 
Client is like a Postman. It is going this object that sends POST request, GET requests.
https://docs.djangoproject.com/en/4.1/topics/testing/tools/

(2)
The argument `companies` comes from api.coronavstech.companies.urls.py from basename="companies".
"companies-list" means we want to get companies' list.
https://www.django-rest-framework.org/api-guide/routers/#api-guide

(3)
We don't have any companies initialized so the response is expected to be an empty list.

(4) We get an error when running the pytest because we need to add Django project to our PYTHONPATH.
We are trying to run Django test with Pytest. 
"""
