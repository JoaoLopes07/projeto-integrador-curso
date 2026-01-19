
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages

User = get_user_model()

class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.home_url = reverse('home')  
        self.redirect_url = '/redirect/'  
        
        # Usuário para testes de login
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'TestPass123!'
        }
        self.user = User.objects.create_user(**self.user_data)
    
    # TESTES DE REGISTRO 
    
    def test_register_view_get(self):
        """Testa acesso GET à página de registro"""
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')
        self.assertContains(response, 'form')
    
    def test_register_view_post_success(self):
        """Testa registro bem-sucedido"""
        data = {
            'username': 'novousuario',
            'email': 'novo@exemplo.com',
            'telefone': '(11) 99999-9999',
            'password1': 'SenhaForte123!',
            'password2': 'SenhaForte123!'
        }
        response = self.client.post(self.register_url, data)
        
        # Verifica redirecionamento 
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url in [self.redirect_url, self.home_url])
        
        # Verifica se usuário foi criado
        self.assertTrue(User.objects.filter(username='novousuario').exists())
    
    def test_register_view_post_success_with_follow(self):
        """Testa registro bem-sucedido seguindo o redirecionamento"""
        data = {
            'username': 'novousuario2',
            'email': 'novo2@exemplo.com',
            'password1': 'SenhaForte123!',
            'password2': 'SenhaForte123!'
        }
    
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 302)
        
        # Verifica se usuário foi criado
        self.assertTrue(User.objects.filter(username='novousuario2').exists())
    
    def test_register_view_post_invalid_data(self):
        """Testa registro com dados inválidos"""
        data = {
            'username': '',  # Inválido
            'email': 'email-invalido',
            'password1': '123',
            'password2': '456'  # Não coincide
        }
        response = self.client.post(self.register_url, data)
        
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(email='email-invalido').exists())
        
        # Verifica se há erros no formulário
        self.assertIn('form', response.context)
        form = response.context['form']
        self.assertFalse(form.is_valid())
    
    def test_register_view_authenticated_user(self):
        """Testa que usuário autenticado é redirecionado - CORRIGIDO"""
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(self.register_url)
        
        #verifica redirecionamento
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url in [self.redirect_url, self.home_url])
    
    def test_register_email_already_exists(self):
        """Testa registro com email já existente"""

        # Primeiro cria um usuário
        existing_email = 'existente@exemplo.com'
        User.objects.create_user(
            username='existente',
            email=existing_email,
            password='pass123'
        )
        
        # Tenta registrar com mesmo email
        data = {
            'username': 'novousuario',
            'email': existing_email,
            'password1': 'SenhaForte123!',
            'password2': 'SenhaForte123!'
        }
        response = self.client.post(self.register_url, data)
        
        self.assertEqual(response.status_code, 200)
        
        # Verifica erro no formulário
        form = response.context['form']
        self.assertIn('email', form.errors)
        self.assertIn('Este email já está em uso.', form.errors['email'])
    
    # TESTES DE LOGIN
    
    def test_login_view_get(self):
        """Testa acesso GET à página de login"""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
    
    def test_login_view_post_success(self):
        """Testa login bem-sucedido"""
        data = {
            'username': 'testuser',
            'password': 'TestPass123!'
        }
        response = self.client.post(self.login_url, data)
        
        # Verifica redirecionamento 
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url in [self.redirect_url, self.home_url])
    
    def test_login_view_post_success_with_session(self):
        """Testa login verificando sessão"""
        data = {
            'username': 'testuser',
            'password': 'TestPass123!'
        }
        response = self.client.post(self.login_url, data)
        
        # Verifica que o usuário está na sessão
        self.assertIn('_auth_user_id', self.client.session)
        self.assertEqual(str(self.user.id), self.client.session['_auth_user_id'])
    
    def test_login_view_post_invalid_credentials(self):
        """Testa login com credenciais inválidas - CORRIGIDO"""
        data = {
            'username': 'testuser',
            'password': 'senhaerrada'
        }
        response = self.client.post(self.login_url, data)
        
        self.assertEqual(response.status_code, 200)
        
        self.assertContains(
            response, 
            'Por favor, entre com um usuário e senha corretos. Note que ambos os campos diferenciam maiúsculas e minúsculas.', 
            html=True
        )
        
        # verifica se há alguma mensagem de erro
        self.assertContains(response, 'alert alert-danger')
    
    def test_login_with_next_parameter(self):
        """Testa login com parâmetro next válido"""
        next_url = reverse('profile')
        login_url = f"{self.login_url}?next={next_url}"
        
        data = {
            'username': 'testuser',
            'password': 'TestPass123!'
        }
        response = self.client.post(login_url, data)
        
        # Deve redirecionar para o next_url (profile)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, next_url)
    
    def test_login_with_invalid_next_parameter(self):
        """Testa login com next URL inválido ou externo"""
        # Testa sem next primeiro
        data = {
            'username': 'testuser',
            'password': 'TestPass123!'
        }
        response = self.client.post(self.login_url, data)
        
        self.assertEqual(response.status_code, 302)
        
    
    def test_login_view_authenticated_user(self):
        """Testa que usuário já autenticado é redirecionado - CORRIGIDO"""
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(self.login_url)
        
        # Verifica redirecionamento
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url in [self.redirect_url, self.home_url])
    
    # TESTES DE LOGOUT
    
    def test_logout_view(self):
        """Testa logout"""
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(self.logout_url)
        
        # Redireciona para login
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('login'))
    
    def test_logout_view_with_follow(self):
        """Testa logout seguindo redirecionamento"""
        self.client.login(username='testuser', password='TestPass123!')
        
        # Faz logout sem follow primeiro
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)
        
        # Agora faz logout e segue para login
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(self.logout_url, follow=True)
        
        # Verifica que seguiu para login
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
    
    def test_logout_unauthenticated(self):
        """Testa logout quando não está autenticado"""
        response = self.client.get(self.logout_url)
        
        # Deve redirecionar para login (com next)
        self.assertEqual(response.status_code, 302)
        expected_url = f"{reverse('login')}?next={self.logout_url}"
        self.assertEqual(response.url, expected_url)