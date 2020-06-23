"""
API V1: Test User
"""
###
# Libraries
###
from os.path import (
    dirname,
    join,
)
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from allauth.account.models import (
    EmailAddress,
)

User = get_user_model()


###
# Test Cases
###
class UserTestCase(APITestCase):
    def setUp(self):
        self.password = 'testuser'
        self.user = User.objects.create(
            username='testuser',
            email='testuser@example.com',
        )
        self.user.set_password(self.password)
        self.user.save()
        Token.objects.create(user=self.user)

        self.user2 = User.objects.create(
            username='testuser2',
            email='testuser2@example.com',
        )
        self.user2.set_password(self.password)
        self.user2.save()
        Token.objects.create(user=self.user2)

        self.base_dir = dirname(dirname(dirname(dirname(dirname(__file__)))))
        self.image = join(self.base_dir, 'test.png')

    def test_sign_up_sucess(self):
        url = reverse('rest_register')
        payload = {
            'email': 'user@test.com',
            'password1': self.password,
            'password2': self.password,
        }
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        emailaddress = EmailAddress.objects.filter(email=payload.get('email'))
        self.assertEqual(True, emailaddress.exists())

    def test_sign_up_wrong_email(self):
        url = reverse('rest_register')
        payload = {
            'email': 'usertest.com',
            'password1': self.password,
            'password2': self.password,
        }
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sign_up_missing_email(self):
        url = reverse('rest_register')
        payload = {
            'password1': self.password,
            'password2': self.password,
        }
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sign_up_repeated_email(self):
        url = reverse('rest_register')
        payload = {
            'email': self.user.email,
            'password1': self.password,
            'password2': self.password,
        }
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sign_up_different_passwords(self):
        url = reverse('rest_register')
        payload = {
            'email': 'user@test.com',
            'password1': self.password,
            'password2': f'{self.password}1',
        }
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sign_up_missing_password(self):
        url = reverse('rest_register')
        payload = {
            'email': 'user@test.com',
            'password1': self.password,
        }
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sign_in_success(self):
        url = reverse('rest_login')
        payload = {
            'email': self.user.email,
            'password': self.password,
        }
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data.get('user').get('email'), payload.get('email'))

    def test_sign_in_wrong_email(self):
        url = reverse('rest_login')
        payload = {
            'email': f'{self.user.email}.us',
            'password': self.password,
        }
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sign_in_wrong_password(self):
        url = reverse('rest_login')
        payload = {
            'email': self.user.email,
            'password': f'{self.password}1',
        }
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.auth_token.key)
        url = reverse('rest_user_details')
        payload = {
            'first_name': 'test',
            'last_name': 'user',
        }
        response = self.client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(data.get('first_name'), payload.get('first_name'))
        self.assertEqual(data.get('last_name'), payload.get('last_name'))
