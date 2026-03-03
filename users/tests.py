from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from users.models import User


class UserRegistrationTestCase(APITestCase):
    """
    Test user registration endpoint
    """
    
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('users:register')
        self.valid_payload = {
            'email': 'testuser@example.com',
            'password': 'TestPass123!',
            'password_confirm': 'TestPass123!',
            'first_name': 'Test',
            'last_name': 'User'
        }
    
    def test_user_registration_success(self):
        """Test successful user registration"""
        response = self.client.post(
            self.register_url,
            self.valid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user']['email'], self.valid_payload['email'])
        
        # Verify user was created in database
        self.assertTrue(User.objects.filter(email=self.valid_payload['email']).exists())
    
    def test_user_registration_password_mismatch(self):
        """Test registration fails when passwords don't match"""
        invalid_payload = self.valid_payload.copy()
        invalid_payload['password_confirm'] = 'DifferentPass123!'
        
        response = self.client.post(
            self.register_url,
            invalid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_user_registration_duplicate_email(self):
        """Test registration fails with duplicate email"""
        # Create first user
        User.objects.create_user(
            email=self.valid_payload['email'],
            password=self.valid_payload['password']
        )
        
        # Try to register with same email
        response = self.client.post(
            self.register_url,
            self.valid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserLoginTestCase(APITestCase):
    """
    Test user login endpoint
    """
    
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('users:login')
        self.user_data = {
            'email': 'testuser@example.com',
            'password': 'TestPass123!'
        }
        self.user = User.objects.create_user(**self.user_data)
    
    def test_user_login_success(self):
        """Test successful user login"""
        response = self.client.post(
            self.login_url,
            self.user_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user']['email'], self.user_data['email'])
    
    def test_user_login_invalid_credentials(self):
        """Test login fails with invalid credentials"""
        invalid_data = {
            'email': self.user_data['email'],
            'password': 'WrongPassword123!'
        }
        response = self.client.post(
            self.login_url,
            invalid_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_user_login_nonexistent_user(self):
        """Test login fails for nonexistent user"""
        nonexistent_data = {
            'email': 'nonexistent@example.com',
            'password': 'TestPass123!'
        }
        response = self.client.post(
            self.login_url,
            nonexistent_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserLogoutTestCase(APITestCase):
    """
    Test user logout endpoint
    """
    
    def setUp(self):
        self.client = APIClient()
        self.logout_url = reverse('users:logout')
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='TestPass123!'
        )
    
    def test_user_logout_success(self):
        """Test successful user logout"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_user_logout_unauthenticated(self):
        """Test logout fails when not authenticated"""
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CurrentUserTestCase(APITestCase):
    """
    Test current user endpoint
    """
    
    def setUp(self):
        self.client = APIClient()
        self.current_user_url = reverse('users:current-user')
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='TestPass123!',
            first_name='Test',
            last_name='User'
        )
    
    def test_get_current_user(self):
        """Test retrieving current user data"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.current_user_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)
        self.assertEqual(response.data['first_name'], self.user.first_name)
    
    def test_update_current_user(self):
        """Test updating current user data"""
        self.client.force_authenticate(user=self.user)
        update_data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'bio': 'New bio'
        }
        response = self.client.patch(
            self.current_user_url,
            update_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, update_data['first_name'])
        self.assertEqual(self.user.bio, update_data['bio'])
    
    def test_current_user_unauthenticated(self):
        """Test accessing current user when not authenticated"""
        response = self.client.get(self.current_user_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ChangePasswordTestCase(APITestCase):
    """
    Test password change endpoint
    """
    
    def setUp(self):
        self.client = APIClient()
        self.change_password_url = reverse('users:change-password')
        self.old_password = 'OldPass123!'
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password=self.old_password
        )
    
    def test_change_password_success(self):
        """Test successful password change"""
        self.client.force_authenticate(user=self.user)
        data = {
            'old_password': self.old_password,
            'new_password': 'NewPass123!',
            'new_password_confirm': 'NewPass123!'
        }
        response = self.client.post(
            self.change_password_url,
            data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(data['new_password']))
    
    def test_change_password_wrong_old_password(self):
        """Test password change fails with wrong old password"""
        self.client.force_authenticate(user=self.user)
        data = {
            'old_password': 'WrongPass123!',
            'new_password': 'NewPass123!',
            'new_password_confirm': 'NewPass123!'
        }
        response = self.client.post(
            self.change_password_url,
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_change_password_mismatch(self):
        """Test password change fails when new passwords don't match"""
        self.client.force_authenticate(user=self.user)
        data = {
            'old_password': self.old_password,
            'new_password': 'NewPass123!',
            'new_password_confirm': 'DifferentPass123!'
        }
        response = self.client.post(
            self.change_password_url,
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
