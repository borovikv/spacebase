from django.contrib.auth.models import User
from django.test import Client, TestCase

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
            user=self.user, name='Max Mustermann', street_address='456 Randomstreet', city='Giventown')
        self.assertEquals(result, expected)

    def test_find_by_address_when_address_is_null(self):
        UserAddress.objects.create(user=self.user, name='Max', street_address='Otherstreet', city='Giventown')
        expected = UserAddress.objects.create(user=self.user, name='Max', city='Giventown')
        result = UserAddress.find(user=self.user, name='Max', street_address='Randomstreet', city='Giventown')
        self.assertEquals(result, expected)

    def test_find_by_address_when_different_address(self):
        UserAddress.objects.create(user=self.user, name='Max', street_address='456 Randomstreet', city='Giventown')
        result = UserAddress.find(user=self.user, name='Max', street_address='789 Otherstreet', city='Giventown')
        self.assertIsNone(result)

    def test_find_by_address_when_different_street_and_same_number(self):
        UserAddress.objects.create(user=self.user, name='Max', street_address='789 Randomstreet', city='Giventown')
        result = UserAddress.find(user=self.user, name='Max', street_address='789 Otherstreet', city='Giventown')
        self.assertIsNone(result)

    def test_find_by_street_address_line2(self):
        expected = UserAddress.objects.create(user=self.user, name='Max', city='Giventown')
        result = UserAddress.find(user=self.user, name='Max', street_address_line2='Randomstreet', city='Giventown')
        self.assertEquals(result, expected)

    def test_find_by_zipcode(self):
        expected = UserAddress.objects.create(user=self.user, name='Max', city='Giventown')
        result = UserAddress.find(user=self.user, name='Max', zipcode='1234', city='Giventown')
        self.assertEquals(result, expected)

    def test_find_by_city(self):
        expected = UserAddress.objects.create(user=self.user, name='Max', city='Francisco')
        result = UserAddress.find(user=self.user, name='Max', city='San Francisco')
        self.assertEquals(result, expected)

    def test_find_by_state(self):
        expected = UserAddress.objects.create(user=self.user, name='Max', city='Giventown')
        result = UserAddress.find(user=self.user, name='Max', state='DE', city='Giventown')
        self.assertEquals(result, expected)


class TestUserAddressAdmin(TestCase):
    def post(self, **kwargs):
        return self.client.post('/admin/addresses/useraddress/add/', kwargs, follow=True)

    def setUp(self):
        self.user = User.objects.create_user(username='user')
        User.objects.create_superuser('admin', 'admin@example.com', 'Password123')
        self.client = Client()
        self.client.login(username='admin', password='Password123')

    def tearDown(self):
        self.client.logout()

    def test_create_new_object(self):
        self.assertEquals(UserAddress.objects.all().count(), 0)
        self.post(name='Max', city='Giventown')
        self.assertEquals(UserAddress.objects.all().count(), 1)

    def test_deduplication(self):
        self.post(name='Max', city='Giventown')
        self.post(name='Max Mustermann', street_address='Randomstreet', city='Giventown')
        self.post(name='Max Mustermann', street_address='456 Randomstreet', city='Giventown')
        self.post(name='Max Mustermann', street_address='789 Otherstreet', city='Giventown', country='NL')
        result = UserAddress.objects.all()
        self.assertEquals(result.count(), 2)
        self.assertEquals(result.filter(street_address='456 Randomstreet').count(), 1)
        self.assertEquals(result.filter(street_address='789 Otherstreet').count(), 1)
