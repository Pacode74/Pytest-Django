import json
from unittest import TestCase
from django.test import Client
from django.urls import reverse
import pytest
import logging
from api.coronavstech.companies.models import Company
from api.coronavstech.companies.exception_logging.exception_logging_info_level import function_that_logs_something_info_level
from api.coronavstech.companies.exception_logging.exception_logging_warning_level import function_that_logs_something_warning_level
from api.coronavstech.companies.exception_logging.logging_func import logger
from api.coronavstech.companies.exception_logging.raise_covid19_exception import raise_covid19_exception

"""
Look at explanation in notebook 'Pytest automatic testing for our Django application_Section 6'
in Step 28 - Pytest that assert Logs'.Cleaning the code logging and raise exception by
separating apps from tests.
"""


@pytest.mark.django_db
class BasicCompanyAPITestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.companies_url = reverse("companies-list")

    def tearDown(self) -> None:
        pass


class TestGetCompanies(BasicCompanyAPITestCase):
    def test_zero_companies_should_return_empty_list(self) -> None:
        """Test that we GET zero companies. If we fetch the GET request we expect to get empty list."""
        # companies_url = "http://127.0.0.1:8000/companies/"
        response = self.client.get(self.companies_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), [])

    def test_one_company_exists_should_succeed(self) -> None:
        """We want to have one company in our test database and
        when we retrieve it we want to return just one company.
        """
        test_company = Company.objects.create(name="Amazon")
        response = self.client.get(self.companies_url)
        print(response.content)
        response_content = json.loads(response.content)[0]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_content.get("name"), test_company.name)
        self.assertEqual(response_content.get("status"), "Hiring")
        self.assertEqual(response_content.get("application_link"), "")
        self.assertEqual(response_content.get("notes"), "")
        test_company.delete()


class TestPostCompanies(BasicCompanyAPITestCase):
    def test_create_company_without_arguments_should_fail(self) -> None:
        """If we POST request of creating new company without a body in Postman
        we will get a response "name": ["This field is required"].
        This is what we are going to test. Response status should be 400"""
        response = self.client.post(path=self.companies_url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content), {"name": ["This field is required."]}
        )

    def test_create_existing_company_should_fail(self) -> None:
        """
        If we POST request of creating existing company, we will get in the Postman
        "name": ["company with this name already exists."]. Response status 400.
        This is what we are going to test.
        """
        Company.objects.create(name="apple")
        response = self.client.post(path=self.companies_url, data={"name": "apple"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content),
            {"name": ["company with this name already exists."]},
        )

    def test_create_company_with_only_name_all_fields_should_be_default(self)->None:
        response = self.client.post(path=self.companies_url, data={"name": "test company name"})
        print(response.content)
        response_content = json.loads(response.content)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_content.get("name"), "test company name")
        self.assertEqual(response_content.get("status"), "Hiring")
        self.assertEqual(response_content.get("application_link"), "")
        self.assertEqual(response_content.get("notes"), "")

    def test_create_company_with_layoffs_status_should_succeed(self)-> None:
        response = self.client.post(path=self.companies_url, data={"name": "test company name", "status": "Layoffs"})
        print(response.content)
        response_content = json.loads(response.content)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_content.get("status"), "Layoffs")

    def test_create_company_with_wrong_status_should_fail(self) -> None:
        response = self.client.post(path=self.companies_url, data={"name": "test company name", "status": "WrongStatus"})
        print(f'response.content:{response.content}')
        self.assertEqual(response.status_code, 400)
        self.assertIn("WrongStatus", str(response.content))
        self.assertIn("is not a valid choice", str(response.content))

class TestInGeneralMarkXfailAndSkip(BasicCompanyAPITestCase):
    @pytest.mark.xfail(reason="Test is executed but is skipped")
    def test_should_be_ok_if_fails(self)-> None:
        assert 1 == 2
    @pytest.mark.skip
    def test_should_be_skipped(self)-> None:
        assert 1 ==2

class TestInGeneralRaisException(BasicCompanyAPITestCase):
    def test_raise_covid19_exception_should_pass(self)-> None:
        """test that will catch ValueError exception when it is risen
         and test that the text of the exception is correct"""
        with pytest.raises(ValueError) as e:
            raise_covid19_exception()
        assert "CoronaVirus Exception" == str(e.value)

class TestInGeneralExceptionLogging(BasicCompanyAPITestCase):
    @pytest.fixture(autouse=True)
    def inject_fixtures(self, caplog):
        """caplog fixture that you can insert in you
        methods in order to access the captured logs"""
        self._caplog = caplog

    def test_exception_logged_warning_level(self) -> None:
        """Testing exception was raised and logged at WARNING level"""
        function_that_logs_something_warning_level()
        assert "I am logging CoronaVirus Exception" in self._caplog.text

    def test_exception_logged_info_level(self) -> None:
        """Testing exception was raised and logged at INFO level"""
        with self._caplog.at_level(logging.INFO):
            function_that_logs_something_info_level()
            print(f'self._caplog.text:{self._caplog.text}')
            assert "I am logging CoronaVirus Exception" in self._caplog.text

    def test_logged_info_level(self) -> None:
        """Testing logging function at INFO level"""
        with self._caplog.at_level(logging.INFO):
            logger() # imported from exception_logging
            print(f'self._caplog.text:{self._caplog.text}')
            assert "I am logging info level" in self._caplog.text



