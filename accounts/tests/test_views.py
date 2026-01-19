from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class ProtectedViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.home_url = reverse('home')
        self.profile_url = reverse('profile')
        
        # Cria e loga usuário
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123!'
        )
    
    def test_home_view_authenticated(self):
        """Testa acesso à home quando autenticado"""
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(self.home_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/home.html')
    
    def test_home_view_unauthenticated(self):
        """Testa que home redireciona quando não autenticado"""
        response = self.client.get(self.home_url)
        
        # Deve redirecionar para login (com next)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)
    
    def test_profile_view_authenticated(self):
        """Testa acesso ao perfil quando autenticado"""
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(self.profile_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')
    
    def test_profile_view_unauthenticated(self):
        """Testa que perfil redireciona quando não autenticado"""
        response = self.client.get(self.profile_url)
        
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)