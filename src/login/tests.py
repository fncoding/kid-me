from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class RegistrationTests(TestCase):
    def test_register_view_get(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login/register.html')

    def test_register_view_post(self):
        response = self.client.post(reverse('register'), {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'Testpasswort123!',
            'password2': 'Testpasswort123!',
        })
        # Nach erfolgreicher Registrierung wird weitergeleitet
        self.assertEqual(response.status_code, 302)
        # User wurde angelegt (aber noch nicht aktiviert)
        self.assertTrue(User.objects.filter(username='testuser').exists())