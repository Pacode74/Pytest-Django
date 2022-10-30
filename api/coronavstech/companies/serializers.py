from rest_framework import serializers
from .models import Company


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company  # (1)
        fields = ["id", "name", "status", "application_link", "last_update", "notes"]  # (2)


"""
Notes:
(1) specify which model you wan to serialize. 
(2) this is what we want to serialize.
"""
