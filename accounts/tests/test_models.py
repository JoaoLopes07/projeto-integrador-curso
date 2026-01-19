from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserModelTest(TestCase):
    def test_create_user(self):
        """Testa a criação de um usuário normal"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('password123'))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertEqual(user.role, 'afiliado')  #padrao
    
    def test_create_superuser(self):
        """Testa a criação de um superusuário"""
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
    
    def test_email_unique_constraint(self):
        """Testa que o email deve ser único"""
        User.objects.create_user(
            username='user1',
            email='same@email.com',
            password='pass123'
        )
        
        with self.assertRaises(Exception):  # IntegrityError
            User.objects.create_user(
                username='user2',
                email='same@email.com',  # Email duplicado
                password='pass456'
            )
    
    def test_role_choices(self):
        """Testa os valores permitidos para o campo role"""
        user = User.objects.create_user(
            username='testrole',
            email='role@test.com',
            password='pass123',
            role='diretoria'
        )
        self.assertEqual(user.role, 'diretoria')
        
        # Testa valor inválido
        user.role = 'invalido'
        with self.assertRaises(ValidationError):
            user.full_clean()  # Valida os campos
    
    def test_string_representation(self):
        """Testa a representação em string do modelo"""
        user = User.objects.create_user(
            username='john',
            email='john@doe.com',
            password='pass123'
        )
        self.assertEqual(str(user), 'john@doe.com')  # usa email como string