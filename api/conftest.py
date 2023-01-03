from api.coronavstech.companies.models import Company
import pytest
from typing import List

@pytest.fixture
def amazon() -> Company:
    """Fixture value is fixed on amazon"""
    return Company.objects.create(name="Amazon")


@pytest.fixture
def company(**kwargs):
    """Fixture that receives an argument of a name, and
    it will return us the company with that name.
    This fixture returns a function which takes some arguments
    and that function return us a company"""

    def _company_factory(**kwargs) -> Company:
        company_name = kwargs.pop("name", "Test Company INC")
        return Company.objects.create(name=company_name, **kwargs)

    return _company_factory


@pytest.fixture
def companies(request, company) -> List[Company]:
    """This fixture will use company fixture. company fixture return
    the company with the name. Pytest request is an object holding a metadata
    of our test. This is a way to pass parameters into the fixture."""
    companies = []
    names = request.param
    print(f"{names=}")
    for name in names:
        companies.append(company(name=name))
    return companies  # companies will hold a list of companies
