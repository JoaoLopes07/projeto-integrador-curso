
from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.forms import CustomUserCreationForm

User = get_user_model()

class CustomUserCreationFormTest(TestCase):
    def test_form_valid_data(self):
        """Testa o formulário com dados válidos"""
        form_data = {
            'username': 'novousuario',
            'email': 'novo@exemplo.com',
            'telefone': '(11) 99999-9999',
            'password1': 'SenhaForte123!',
            'password2': 'SenhaForte123!'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_form_email_unique(self):
        """Testa validação de email único"""
        # Cria um usuário existente
        User.objects.create_user(
            username='existente',
            email='existente@exemplo.com',
            password='pass123'
        )
        
        # Tenta criar outro com mesmo email
        form_data = {
            'username': 'novousuario',
            'email': 'existente@exemplo.com',  # Email já existe!
            'password1': 'SenhaForte123!',
            'password2': 'SenhaForte123!'
        }
        form = CustomUserCreationForm(data=form_data)
        
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertIn('Este email já está em uso.', form.errors['email'])
    
    def test_form_passwords_mismatch(self):
        """Testa quando as senhas não coincidem"""
        form_data = {
            'username': 'testuser',
            'email': 'test@exemplo.com',
            'password1': 'Senha123',
            'password2': 'Senha456'  # Diferente!
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
    
    def test_form_missing_required_fields(self):
        """Testa campos obrigatórios"""
        form_data = {
            'username': '',  # Campo obrigatório vazio
            'email': 'email@exemplo.com',
            'password1': 'Senha123',
            'password2': 'Senha123'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
    
    def test_form_telefone_optional(self):
        """Testa que telefone é opcional"""
        form_data = {
            'username': 'testuser',
            'email': 'test@exemplo.com',
            'password1': 'SenhaForte123!',
            'password2': 'SenhaForte123!'
            # telefone não fornecido
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        # Salva para verificar
        user = form.save()
        self.assertEqual(user.telefone, '')
    
    def test_form_field_widgets(self):
        """Testa que os widgets estão configurados corretamente"""
        form = CustomUserCreationForm()
        
        # Verifica classes CSS nos widgets
        self.assertIn('form-control', str(form.fields['email'].widget.attrs))
        self.assertIn('form-control', str(form.fields['telefone'].widget.attrs))