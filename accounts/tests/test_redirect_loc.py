def test_redirect_diagnostic(self):
    """Teste para descobrir para onde está redirecionando"""
    data = {
        'username': 'testuser',
        'password': 'TestPass123!'
    }
    response = self.client.post(self.login_url, data)
    print(f"Status: {response.status_code}")
    print(f"Redirect URL: {response.url}")
    print(f"Location header: {response.headers.get('Location')}")