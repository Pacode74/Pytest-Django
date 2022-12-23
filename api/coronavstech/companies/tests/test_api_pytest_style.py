import json
from django.urls import reverse
import pytest
import logging
from api.coronavstech.companies.models import Company
from api.coronavstech.companies.exception_logging.exception_logging_info_level import (
    function_that_logs_something_info_level,
)
from api.coronavstech.companies.exception_logging.exception_logging_warning_level import (
    function_that_logs_something_warning_level,
)
from api.coronavstech.companies.exception_logging.logging_func import logger
from api.coronavstech.companies.exception_logging.raise_covid19_exception import (
    raise_covid19_exception,
)

"""
Look at explanation in notebook 'Pytest automatic testing for our Django application_Section 6'
in Step 30 - Refractoring our unittest code to pytest code. Migrating tests to native Pytest.
"""

companies_url = reverse("companies-list")
pytestmark = pytest.mark.django_db


# ------TestGetCompanies-----------------------
def test_zero_companies_should_return_empty_list(client) -> None:
    """Test that we GET zero companies. If we fetch the GET request we expect to get empty list."""
    # companies_url = "http://127.0.0.1:8000/companies/"
    response = client.get(companies_url)
    assert response.status_code == 200
    assert json.loads(response.content) == []


def test_one_company_exists_should_succeed(client) -> None:
    """We want to have one company in our test database and
    when we retrieve it we want to return just one company.
    """
    test_company = Company.objects.create(name="Amazon")
    response = client.get(companies_url)
    print(response.content)
    response_content = json.loads(response.content)[0]
    assert response.status_code == 200
    assert response_content.get("name") == test_company.name
    assert response_content.get("status") == "Hiring"
    assert response_content.get("application_link") == ""
    assert response_content.get("notes") == ""


# ------TestPostCompanies---------------------------
def test_create_company_without_arguments_should_fail(client) -> None:
    """If we POST request of creating new company without a body in Postman
    we will get a response "name": ["This field is required"].
    This is what we are going to test. Response status should be 400"""
    response = client.post(path=companies_url)
    assert response.status_code == 400
    assert json.loads(response.content) == {"name": ["This field is required."]}


def test_create_existing_company_should_fail(client) -> None:
    """
    If we POST request of creating existing company, we will get in the Postman
    "name": ["company with this name already exists."]. Response status 400.
    This is what we are going to test.
    """
    Company.objects.create(name="apple")
    response = client.post(path=companies_url, data={"name": "apple"})
    assert response.status_code == 400
    assert json.loads(response.content) == {
        "name": ["company with this name already exists."]
    }


def test_create_company_with_only_name_all_fields_should_be_default(client) -> None:
    response = client.post(path=companies_url, data={"name": "test company name"})
    print(response.content)
    response_content = json.loads(response.content)
    assert response.status_code == 201
    assert response_content.get("name") == "test company name"
    assert response_content.get("status") == "Hiring"
    assert response_content.get("application_link") == ""
    assert response_content.get("notes") == ""


def test_create_company_with_layoffs_status_should_succeed(client) -> None:
    response = client.post(
        path=companies_url,
        data={"name": "test company name", "status": "Layoffs"},
    )
    print(response.content)
    response_content = json.loads(response.content)
    assert response.status_code == 201
    assert response_content.get("status") == "Layoffs"


def test_create_company_with_wrong_status_should_fail(client) -> None:
    response = client.post(
        path=companies_url,
        data={"name": "test company name", "status": "WrongStatus"},
    )
    print(f"response.content:{response.content}")
    assert response.status_code == 400
    assert "WrongStatus" in str(response.content)
    assert "is not a valid choice" in str(response.content)


# ------TestInGeneralMarkXfailAndSkip-------------------------
@pytest.mark.xfail(reason="Test is executed but is skipped")
def test_should_be_ok_if_fails() -> None:
    assert 1 == 2


@pytest.mark.skip
def test_should_be_skipped() -> None:
    assert 1 == 2


# ------TestInGeneralRaisException-----------------------
def test_raise_covid19_exception_should_pass() -> None:
    """test that will catch ValueError exception when it is risen
    and test that the text of the exception is correct"""
    with pytest.raises(ValueError) as e:
        raise_covid19_exception()
    assert "CoronaVirus Exception" == str(e.value)


# -----TestInGeneralExceptionLogging--------------------
def test_exception_logged_warning_level(caplog) -> None:
    """Testing exception was raised and logged at WARNING level"""
    function_that_logs_something_warning_level()
    assert "I am logging CoronaVirus Exception" in caplog.text


def test_exception_logged_info_level(caplog) -> None:
    """Testing exception was raised and logged at INFO level"""
    with caplog.at_level(logging.INFO):
        function_that_logs_something_info_level()
        print(f".caplog.text:{caplog.text}")
        assert "I am logging CoronaVirus Exception" in caplog.text


def test_logged_info_level(caplog) -> None:
    """Testing logging function at INFO level"""
    with caplog.at_level(logging.INFO):
        logger()  # imported from exception_logging
        print(f".caplog.text:{caplog.text}")
        assert "I am logging info level" in caplog.text
