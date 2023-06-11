import unittest
import bcrypt
from flask import url_for
from flask_login import current_user
from flask_testing import TestCase
from app import app, db
from models import User
from forms import RegisterForm, LoginForm


class AuthTestCase(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def setUp(self):
        db.create_all()
        self.client = self.app.test_client()
        self.register_form = RegisterForm()
        self.login_form = LoginForm()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_login(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('auth.html')
        self.assertIsInstance(response.context['form'], LoginForm)

    def test_login_invalid_credentials(self):
        user = User(username='test1234', email='test@example.com', password='password1234')
        db.session.add(user)
        db.session.commit()

        response = self.client.post('/login/', data={'email': 'test@example.com', 'password': 'wrong_password'})
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('auth.html')
        self.assertIn(b'Invalid Username or password!', response.data)

    def test_login_valid_credentials(self):
        password = 'password1234'
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username='test', email='test@example.com', password=hashed_password)
        db.session.add(user)
        db.session.commit()

        response = self.client.post('/login/', data={'email': 'test@example.com', 'password': password}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('home.html')
        self.assertEqual(current_user.username, 'test')

    def test_register(self):
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('auth.html')
        self.assertIsInstance(response.context['form'], RegisterForm)

    def test_register_valid_form(self):
        response = self.client.post('/register/', data={'username': 'test', 'email': 'test@example.com', 'password': 'password1234'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('home.html')
        self.assertTrue(User.query.filter_by(email='test@example.com').first())

    def test_logout(self):
        response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('auth.html')
        self.assertIsNone(current_user.get_id())


if __name__ == '__main__':
    unittest.main()
