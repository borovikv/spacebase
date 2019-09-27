import operator
from functools import reduce

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q


class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    street_address = models.CharField(max_length=255, blank=True, null=True)
    street_address_line2 = models.CharField(max_length=255, blank=True, null=True)
    zipcode = models.CharField(max_length=12, blank=True, null=True)
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=64, blank=True, null=True)
    country = models.CharField(max_length=2, blank=True, null=True)
    full_address = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        streetdata = f"{self.street_address}\n{self.street_address_line2}"
        self.full_address = f"{streetdata}\n{self.zipcode} {self.city} {self.state} {self.country}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    @staticmethod
    def find(user, **kwargs):
        queries = [UserAddress.build_query(key, value) for key, value in kwargs.items()]
        result = UserAddress.objects.filter(*queries, user=user)
        return result.first()

    @staticmethod
    def build_query(field_name, value):
        result = Q(**{field_name: value})
        if UserAddress._meta.get_field(field_name).null:
            result |= Q(**{f'{field_name}__isnull': True})
        return result | reduce(operator.or_, [Q(**{field_name: s}) for s in value.split()])
