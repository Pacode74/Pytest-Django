from django.db import models
from django.db.models import URLField
from django.utils.timezone import now


class Company(models.Model):
    """Class that creates a model called Company."""

    class CompanyStatus(models.TextChoices):
        LAYOFFS = "Layoffs"
        HIRING_FREEZE = "Hiring Freeze"
        HIRING = "Hiring"

    name = models.CharField(max_length=30, unique=True)
    status = models.CharField(
        choices=CompanyStatus.choices, default=CompanyStatus.HIRING, max_length=30
    )  # (1)
    last_update = models.DateTimeField(default=now, editable=True)  # (2)
    application_link = URLField(blank=True)  # (3)
    notes = models.CharField(max_length=100, blank=True)

    def __str__(self) -> str:
        """Function that overrides __str__ function
        and adds/fixes identifier for the company's name
        in admin panel"""
        return f"{self.name}"


"""
Notes:
(1) - max_length is required parameter in CharField.
(2) - https://docs.djangoproject.com/en/4.1/ref/models/fields/
(3) - blank=True means it can be an empty string.
"""
