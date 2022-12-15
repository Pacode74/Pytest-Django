from django.core.mail import send_mail
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from api.coronavstech.companies.models import Company
from api.coronavstech.companies.serializers import CompanySerializer


class CompanyViewSet(ModelViewSet):
    serializer_class = CompanySerializer  # (1)
    queryset = Company.objects.all().order_by("-last_update")  # (2)
    pagination_class = PageNumberPagination  # (3)

@api_view(http_method_names=["POST"])
def send_company_email(request: Request)->Response:
    """
    Function that will send email with request payload.
    With the help of REST FRAMEWORK decorator `@api_view()`
    we will treat our function as POST endpoint.
    sender: pavlo_ivanov@yahoo.com
    receiver: pavlo_ivanov@yahoo.com
    """
    send_mail(subject=request.data.get("subject"), message=request.data.get("message"), from_email="python.testme@gmail.com", recipient_list=["python.testme@gmail.com"])
    return Response({"status": "success", "info": "email sent successfully"}, status=200)





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
This is done so that we don't get timeout as only part of the pages are received at a time. 
"""
