from django import forms
from django.core.exceptions import ValidationError
from django.db import models

IBAN_LENGTH = len('GR9608100010000001234567890')


def clean_value(value):
    if value is None:
        return value
    return value.upper().replace(' ', '').replace('-', '')


def disguise(value):
    return f'---{clean_value(value)[-4:]}'


def validate_iban(value):
    if len(clean_value(value)) != IBAN_LENGTH:
        raise ValidationError('Enter a valid IBAN.', code='invalid')


class IBANFormField(forms.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('min_length', IBAN_LENGTH)
        kwargs.setdefault('max_length', IBAN_LENGTH)
        super(IBANFormField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        value = super(IBANFormField, self).to_python(value)
        return clean_value(value)

    def validate(self, value):
        super().validate(value)
        validate_iban(value)


class DisguiseIBANFormField(IBANFormField):
    def prepare_value(self, value):
        return disguise(value)


class IBANField(models.CharField):
    def __init__(self, *args, **kwargs):
        super(IBANField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'form_class': DisguiseIBANFormField}
        defaults.update(kwargs)
        return super().formfield(**defaults)


class IBAN(models.Model):
    iban = IBANField(max_length=IBAN_LENGTH)

    def __str__(self):
        return disguise(self.iban)
