import os
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

TEST_USER = os.environ.get('DJANGO_TEST_USER', 'loginuser')
TEST_EMAIL = os.environ.get('DJANGO_TEST_EMAIL', 'login@example.com')
TEST_PASSWORD = os.environ.get('DJANGO_TEST_PASSWORD', 'Testpasswort123!')

class RegistrationTests(TestCase):
    def test_register_view_get(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login/register.html')

    def test_register_view_post_success(self):
        response = self.client.post(reverse('register'), {
            'username': 'neueruser',
            'email': 'neueruser@example.com',
            'password1': 'StarkesPasswort123!',
            'password2': 'StarkesPasswort123!',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='neueruser').exists())
        user = User.objects.get(username='neueruser')
        self.assertFalse(user.is_active)  # Account muss erst aktiviert werden

    def test_register_view_post_password_mismatch(self):
        response = self.client.post(reverse('register'), {
            'username': 'user2',
            'email': 'user2@example.com',
            'password1': 'Passwort123!',
            'password2': 'AnderesPasswort!',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'password2', "Die beiden Passwörter sind nicht identisch.")

    def test_register_view_post_existing_username(self):
        User.objects.create_user(username='doppeluser', email='doppel@example.com', password='Passwort123!')
        response = self.client.post(reverse('register'), {
            'username': 'doppeluser',
            'email': 'neu@example.com',
            'password1': 'Passwort123!',
            'password2': 'Passwort123!',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'username', "Dieser Benutzername ist bereits vergeben.")

    def test_register_view_post_invalid_email(self):
        response = self.client.post(reverse('register'), {
            'username': 'user3',
            'email': 'keineemail',
            'password1': 'Passwort123!',
            'password2': 'Passwort123!',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'email', "Bitte gültige E-Mail-Adresse eingeben.")

class LoginTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username=TEST_USER,
            email=TEST_EMAIL,
            password=TEST_PASSWORD
        )
        self.user.is_active = True
        self.user.save()

    def test_login_view_get(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_login_view_post_success(self):
        response = self.client.post(reverse('login'), {
            'username': TEST_USER,
            'password': TEST_PASSWORD,
        })
        self.assertEqual(response.status_code, 302)  # Redirect nach Login

    def test_login_view_post_wrong_password(self):
        response = self.client.post(reverse('login'), {
            'username': 'loginuser',
            'password': 'FalschesPasswort!',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Bitte geben Sie einen gültigen Benutzernamen und ein gültiges Passwort ein.")

    def test_login_view_post_inactive_user(self):
        self.user.is_active = False
        self.user.save()
        response = self.client.post(reverse('login'), {
            'username': 'loginuser',
            'password': 'Testpasswort123!',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Bitte geben Sie einen gültigen Benutzernamen und ein gültiges Passwort ein.")

    def test_login_view_post_nonexistent_user(self):
        response = self.client.post(reverse('login'), {
            'username': 'unbekannt',
            'password': 'irgendwas',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Bitte geben Sie einen gültigen Benutzernamen und ein gültiges Passwort ein.")