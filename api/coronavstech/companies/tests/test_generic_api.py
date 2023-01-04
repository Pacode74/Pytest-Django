import requests
import json
import pytest

"""Important: in order for the test to work you need Django server running.
to run it: $ api/coronavstech/manage.py runserver
"""
testing_env_companies_url = (
    "http://127.0.0.1:8000/companies/"  # pointing to local host Django server
)

@pytest.mark.skip_in_ci
def test_zero_companies_should_return_empty_list_django_agnostic() -> None:
    """Test that we GET zero companies. If we fetch the GET request we expect to get empty list."""
    response = requests.get(url=testing_env_companies_url)
    # print(f"{response.status_code=}")
    assert response.status_code == 200
    # print(f"{json.loads(response.content)=}")
    assert json.loads(response.content) == []
    # assert json.loads(response.content)[0]["id"] == 13

@pytest.mark.skip_in_ci
def test_create_company_with_layoffs_status_should_succeed_django_agnostic() -> None:
    response = requests.post(
        url=testing_env_companies_url,
        json={"name": "test company name", "status": "Layoffs"},
    )
    print(f"{response.content}")
    response_content = json.loads(response.content)
    assert response.status_code == 201
    assert response_content.get("status") == "Layoffs"

    cleanup_company(company_id=response_content["id"])

def cleanup_company(company_id: str)-> None:
    response = requests.delete(url=f"http://127.0.0.1:8000/companies/{company_id}")
    assert response.status_code == 204