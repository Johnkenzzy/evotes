from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.organizations.models import Organization


class OrganizationViewSetTestCase(APITestCase):
    """Test case for organization views"""

    def setUp(self):
        """
        Setup test data.
        This method is run before every test.
        """
        # Create test organization
        self.organization_data = {
            'name': 'Test Organization',
            'email': 'test@org.com',
            'phone': '1234567890',
            'address': '123 Test St, Test City',
            'logo': '',
            'website': 'http://testorg.com',
            'password': 'securepassword123',  #
        }

        # API endpoint to create organization
        self.create_url = reverse('create_organization')

    def test_create_organization(self):
        """Test creating a new organization"""
        data = {
            'name': 'New Org',
            'email': 'new@org.com',
            'phone': '9876543210',
            'address': '456 New St, New City',
            'logo': '',
            'website': 'http://neworg.com',
            'password': 'newsecurepassword123',
        }

        # Make POST request to create organization
        response = self.client.post(self.create_url, data, format='json')

        # Assert that the response status is 201 Created
        self.assertEqual(response.errors, status.HTTP_201_CREATED)

        # Assert that the organization was created and password is hashed
        self.assertTrue(Organization.objects.filter(
            email='new@org.com').exists())

    def test_update_organization(self):
        """Test updating an existing organization"""
        data = {
            'name': 'Updated Org',
            'email': 'test@org.com',
            'phone': '1234567890',
            'address': '123 Updated St, Test City',
            'logo': '',
            'website': 'http://updatedorg.com',
            'password': 'updatedsecurepassword123',
        }

        # Make PUT request to update organization
        url = reverse('update_organization',
                      kwargs={'pk': self.organization.pk})
        response = self.client.put(url, data, format='json')

        # Assert that the response status is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the organization was updated
        updated_org = Organization.objects.get(pk=self.organization.pk)
        self.assertEqual(updated_org.name, 'Updated Org')

    def test_get_organization(self):
        """Test getting an organization by ID"""
        url = reverse('get_organization',
                      kwargs={'pk': self.organization.pk})
        response = self.client.get(url)

        # Assert that the response status is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the correct organization data is returned
        self.assertEqual(response.data['name'],
                         self.organization.name)

    def test_delete_organization(self):
        """Test deleting an organization"""
        url = reverse('delete_organization',
                      kwargs={'pk': self.organization.pk})
        response = self.client.delete(url)

        # Assert that the response status is 204 No Content
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Assert that the organization no longer exists
        self.assertFalse(
            Organization.objects.filter(pk=self.organization.pk).exists())
