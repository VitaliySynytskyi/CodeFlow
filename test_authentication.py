import unittest
from app import app

class TestDataProcessing(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_login_valid_credentials(self):
        # Arrange
        email = "test@example.com"
        password = "password12345"

        # Act
        response = self.app.post("/login/", data=dict(email=email, password=password), follow_redirects=True)

        # Assert
        self.assertEqual(response.status_code, 200)  # Перевірка, що статус-код 200 (OK)
        self.assertEqual(response.request.path, "/login/")  # Перевірка, що відбулося перенаправлення на "/login/"

class TestRegistration(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_register_valid_credentials(self):
        # Arrange
        email = "test@example.com"
        password = "password12345"

        # Act
        response = self.app.post("/register/", data=dict(email=email, password=password), follow_redirects=True)

        # Assert
        self.assertEqual(response.status_code, 200)  # Перевірка, що статус-код 200 (OK)
        self.assertEqual(response.request.path, "/register/")  # Перевірка, що відбулося перенаправлення на "/register/"


if __name__ == "__main__":
    unittest.main()
