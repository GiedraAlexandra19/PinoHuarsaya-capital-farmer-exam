#tests unitarios
import unittest
from app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_index_redirects_without_login(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)  # Redirecciona al login

    def test_login_ok(self):
        response = self.client.post('/login', data={
            'usuario': 'admin',
            'clave': '1234'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
