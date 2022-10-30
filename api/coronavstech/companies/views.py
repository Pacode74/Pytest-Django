from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet

from .models import Company
from serializers import CompanySerializer


class CompanyViewSet(ModelViewSet):
    serializer_class = CompanySerializer  # (1)
    queryset = Company.objects.all().order_by("-last_update")  # (2)
    pagination_class = PageNumberPagination  # (3)


"""
Notes:
(1) here we write the serializer class name from serializers.py.
(2) queryset is what do we want to return. We want to return all the 
companies. Companies.objects.all() is Django Object Relational Mapper(ORM).
It is a way to talk to SQLite3 database instead of making SQL query. 
It is an object oriented obstruction of our database. 

Companies.objects.all() = SELECT * from Company

Then we order them by last update.

(3) we create pages numbers so that our Server is working fast. 
This is done so that we don't get timedout as only part of the pages are received at a time. 
"""