import json
from unittest import TestCase
from django.test import Client
from django.urls import reverse
import pytest

from api.coronavstech.companies.models import Company

"""
Look at explanation in notebook 'Pytest automatic testing for our Django application_Section 6'
in 'Step 23 - Writing our first pytests'
"""

@pytest.mark.django_db
class TestGetCompanies(TestCase):
    def test_zero_companies_should_return_empty_list(self) -> None:
        """Test that we GET zero companies. If we fetch the GET request we expect to get empty list."""
        client = Client()
        # companies_url = "http://127.0.0.1:8000/companies/"
        companies_url = reverse("companies-list")
        response = client.get(companies_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), [])

    def test_one_company_exists_should_succeed(self) -> None:
        """We want to have one company in our test database and
        when we retrieve it we want to return just one company.
        """
        client = Client()
        test_company = Company.objects.create(name="Amazon")
        companies_url = reverse("companies-list")
        response = client.get(companies_url)
        print(response.content)
        response_content = json.loads(response.content)[0]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_content.get("name"), test_company.name)
        self.assertEqual(response_content.get("status"), "Hiring")
        self.assertEqual(response_content.get("application_link"), "")
        self.assertEqual(response_content.get("notes"), "")
        test_company.delete()

