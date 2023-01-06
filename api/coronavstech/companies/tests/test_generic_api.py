import requests
import json
import pytest
import responses


"""Important: in order for the test to work you need Django server running.
to run it: $ api/coronavstech/manage.py runserver
"""
testing_env_companies_url = (
    "http://127.0.0.1:8000/companies/"  # pointing to local host Django server
)


@pytest.mark.skip_in_ci
@pytest.mark.skip(reason="This test needs localhost django server running. Torun the server type"
                         "(Pytest-Django) pavlo@pavlo:~/Documents/Projects/Pytest-Django$ api/coronavstech/"
                         "manage.py runserver")
def test_zero_companies_should_return_empty_list_django_agnostic() -> None:
    """Test that we GET zero companies. If we fetch the GET request we expect to get empty list."""
    response = requests.get(url=testing_env_companies_url)
    # print(f"{response.status_code=}")
    assert response.status_code == 200
    # print(f"{json.loads(response.content)=}")
    assert json.loads(response.content) == []
    # assert json.loads(response.content)[0]["id"] == 13


@pytest.mark.skip_in_ci
@pytest.mark.skip(reason="This test needs localhost django server running. Torun the server type"
                         "(Pytest-Django) pavlo@pavlo:~/Documents/Projects/Pytest-Django$ api/coronavstech/"
                         "manage.py runserver")
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


def cleanup_company(company_id: str) -> None:
    response = requests.delete(url=f"http://127.0.0.1:8000/companies/{company_id}")
    assert response.status_code == 204


@pytest.mark.xfail(reason="api is unstable")
@pytest.mark.crypto
def test_dogecoin_api() -> None:
    """Validate the response from 3rd party service."""
    response = requests.get(
        url="https://api.cryptonator.com/api/ticker/doge-usd",
        headers={"User-Agent": "Mozilla/5.0"},
    )

    assert response.status_code == 200
    response_content = json.loads(response.content)
    assert response_content["ticker"]["base"] == "DOGE"
    assert response_content["ticker"]["target"] == "USD"


@pytest.mark.crypto
@responses.activate
def test_mocked_dogecoin_api() -> None:
    """We expect that the response is in the valid format that we want
    that we are expecting. We are going to test the process after that repsonse.
    We are isolating 3rd party service and we are assuming the response we are getting
    from 3rd party service is a valid response."""
    responses.add(
        method=responses.GET,
        url="https://api.cryptonator.com/api/ticker/doge-usd",
        json={
            "ticker": {
                "base": "PAVLO",
                "target": "PAVLO-USD",
                "price": "0.04535907",
                "volume": "4975940509.75870037",
                "change": "-0.00052372",
            },
            "timestamp": 1612515303,
            "success": True,
            "error": "",
        },
        status=200,
    )
    response = requests.get(
        url="https://api.cryptonator.com/api/ticker/doge-usd",
        headers={"User-Agent": "Mozilla/5.0"},
    )
    assert response.status_code == 200
    response_content = json.loads(response.content)
    assert response_content["ticker"]["base"] == "PAVLO"
    assert response_content["ticker"]["target"] == "PAVLO-USD"

    assert process_crypto() == 29


def process_crypto() -> int:
    response = requests.get(
        url="https://api.cryptonator.com/api/ticker/doge-usd",
        headers={"User-Agent": "Mozilla/5.0"},
    )

    response_content = json.loads(response.content)
    if response.status_code != 200:
        raise ValueError("Request to Crypto API FAILED!")

    coin_name = response_content["ticker"]["base"]
    if coin_name == "PAVLO":
        return 29

    return 42
