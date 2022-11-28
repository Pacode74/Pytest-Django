from rest_framework import routers

from api.coronavstech.companies.views import CompanyViewSet

companies_router = routers.DefaultRouter()  # (1)
companies_router.register(
    "companies", viewset=CompanyViewSet, basename="companies"
)  # (2)

"""
Notes: 
(1) Create a router for our url. DefaultRouter is a bookkeeper 
for all our routers.
(2) we take a companies_router and we want to register a new route.
First, we wan to give it a prefix called 'companies'. 

Second, for the viewset we give it 
CompanyViewSet class name from views.py. 

Third, add basename which is an easy way to access
this url when we are outside of this code. basename going to be very useful when are are going to write our test. 
We are going to use this basename to access 'companies' url. 
"""
