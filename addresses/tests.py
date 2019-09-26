from django.contrib.auth.models import User
from django.test import TestCase

from addresses.models import UserAddress


class TestUserAddressDeduplication(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user')

    def test_find_by_name(self):
        user2 = User.objects.create_user(username='user2')
        UserAddress.objects.create(user=user2, name='Max', city='Giventown')
        expected = UserAddress.objects.create(user=self.user, name='Max', city='Giventown')
        result = UserAddress.find(user=self.user, name='Max Mustermann', city='Giventown')
        self.assertEquals(result, expected)

    def test_find_by_name_is_none(self):
        result = UserAddress.find(user=self.user, name='Max Mustermann', city='Giventown')
        self.assertIsNone(result)

    def test_find_by_address(self):
        UserAddress.objects.create(
            user=self.user, name='Max Mustermann', street_address='Otherstreet', city='Giventown')
        expected = UserAddress.objects.create(
            user=self.user, name='Max Mustermann', street_address='Randomstreet', city='Giventown')
        result = UserAddress.find(
            user=self.user, name='Max Mustermann', street_address='456 Randomstreet', city="Giventown")
        self.assertEquals(result, expected)

    def test_find_by_address_when_address_is_null(self):
        UserAddress.objects.create(user=self.user, name='Max', street_address='Otherstreet', city='Giventown')
        expected = UserAddress.objects.create(user=self.user, name='Max', city='Giventown')
        result = UserAddress.find(user=self.user, name='Max', street_address='Randomstreet', city="Giventown")
        self.assertEquals(result, expected)

    def test_find_by_address_when_different_address(self):
        UserAddress.objects.create(user=self.user, name='Max', street_address='456 Randomstreet', city='Giventown')
        result = UserAddress.find(user=self.user, name='Max', street_address='789 Otherstreet', city="Giventown")
        self.assertIsNone(result)

    def test_find_by_address_when_different_street_and_same_number(self):
        UserAddress.objects.create(user=self.user, name='Max', street_address='789 Randomstreet', city='Giventown')
        result = UserAddress.find(user=self.user, name='Max', street_address='789 Otherstreet', city="Giventown")
        self.assertIsNone(result)

    # def test_find_by_name(self):
    #     UserAddress.objects.create(user=self.user, name='Max', city='Giventown')
    #     UserAddress.objects.create(user=self.user, name='Max Mustermann', city='Giventown')
    #     users = UserAddress.objects.filter(user=self.user).count()
    #     self.assertEquals(users, 1)
