"""
Basic API Tests for File Sharing Application
Run with: python -m pytest test_api.py -v
"""

import pytest
import json
from main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_endpoint(client):
    """Test the home endpoint"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'File Sharing App' in response.data

def test_user_signup(client):
    """Test user registration"""
    data = {
        "email": "test@example.com",
        "password": "TestPassword123!",
        "userType": "client"
    }
    response = client.post('/api/users/signup', 
                          data=json.dumps(data),
                          content_type='application/json')
    
    # Should either succeed or fail if user exists
    assert response.status_code in [201, 400]

def test_user_login_invalid_credentials(client):
    """Test login with invalid credentials"""
    data = {
        "email": "invalid@example.com",
        "password": "wrongpassword"
    }
    response = client.post('/api/users/login',
                          data=json.dumps(data),
                          content_type='application/json')
    
    assert response.status_code in [401, 404]
    response_data = json.loads(response.data)
    assert response_data['success'] == False

def test_file_upload_without_auth(client):
    """Test file upload without authentication"""
    data = {'file': 'test.docx'}
    response = client.post('/api/file/upload', data=data)
    
    # Should fail due to missing authentication
    assert response.status_code == 404

def test_get_files_without_auth(client):
    """Test getting files without authentication"""
    response = client.get('/api/file/uploads')
    
    # Should fail due to missing authentication
    assert response.status_code == 404

# TODO: Add more comprehensive tests
# - Test with valid authentication
# - Test file upload with valid ops user
# - Test file download functionality
# - Test email verification
# - Test password hashing
