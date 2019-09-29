from django.core.exceptions import ValidationError
from django.test import TestCase

import iban.models


class TestModels(TestCase):
    def test_clean_value(self):
        self.assertIsNone(iban.models.clean_value(None))
        self.assertEqual(iban.models.clean_value('1 2 - 3'), '123')

    def test_disguise(self):
        self.assertEqual(iban.models.disguise('GR9608100010000001234567890'), '---7890')

    def test_validate_iban_when_invalid_iban(self):
        with self.assertRaises(ValidationError):
            iban.models.validate_iban('---1234')
