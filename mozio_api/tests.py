from django.test import TestCase

# Create your tests here.
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from mozio_api.models import ProviderModel, ServiceAreaModel
import datetime

import logging
logger = logging.getLogger(__name__)

class ProviderViewSetTests(APITestCase):
    providerId = ''
    def add_test_provider(self):
        """
        Adds a test provider into the database
        """
        logger.debug('Adding a new provider into database')
        p = ProviderModel( name='provider1', 
                    email='provider1@test.com',
                    phoneNumber='123456789',
                    language='EN',
                    currency='USD'
        )
        p.save()
        self.providerId = p.id
        logger.debug('Successfully added test provider into the database')

    def test_list_providers(self):
        """
        Test to list all the providers in the list
        """
        logger.debug('Starting test list providers')

        self.add_test_provider()

        url = 'http://localhost:8000/api/providers/'

        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.get(url, format='json')
        json = response.json()

        logger.debug('Testing status code response: %s, code: %d'%(response, response.status_code))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        logger.debug('Testing result count')
        self.assertEqual(len(json['providers']), 1)

    def test_create_provider(self):
        """
        Tests creating a new provider object
        """
        logger.debug('Starting test create provider')
        url = 'http://localhost:8000/api/providers/'
        data = {
            'name' :'provider1', 
            'email' :'provider1@test.com',
            'phoneNumber' : '123456789',
            'language' : 'EN',
            'currency' : 'USD',
        }

        logger.debug('Sending TEST data to url: %s, data: %s'%(url, data))
        response = self.client.post(url, data, format='json')
   
        logger.debug('Testing status code response: %s, code: %d'%(response, response.status_code))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        logger.debug('Testing provider count to make sure object was successfully added')
        self.assertEqual(ProviderModel.objects.count(), 1)

        logger.debug('Testing new provider object details')
        p = ProviderModel.objects.get()
        self.assertEqual(p.name, 'provider1')
        self.assertEqual(p.email, 'provider1@test.com')
        self.assertEqual(p.phoneNumber, '123456789')
        self.assertEqual(p.language, 'EN')
        self.assertEqual(p.currency, 'USD')

        logger.debug('Test provider create completed successfully')

    def test_delete_providers(self):
        """
        Test to see if deleting works
        """
        logger.debug('Starting test delete providers')

        self.add_test_provider()

        url = 'http://localhost:8000/api/providers/%s'%self.providerId
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.delete(url, format='json')

        logger.debug('Testing to see if status code is correct')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_put_providers(self):
        """
        Test to see if put works
        """
        logger.debug('Starting test put providers')

        self.add_test_provider()

        url = 'http://localhost:8000/api/providers/%s'%self.providerId
        logger.debug('Sending TEST data to url: %s'%url)
        data = {
            'name' :'provider1_update', 
            'email' :'provider1_update@test.com',
            'phoneNumber' : '123456789',
            'language' : 'EN',
            'currency' : 'USD',
        }
        
        response = self.client.patch(url, data, format='json')
        # json = response.json()
        
        logger.debug('Testing to see if status code is correct')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        logger.debug('Testing modified provider object details')
        p = ProviderModel.objects.get()
        self.assertEqual(p.name, 'provider1_update')
        self.assertEqual(p.email, 'provider1_update@test.com')
        self.assertEqual(p.phoneNumber, '123456789')
        self.assertEqual(p.language, 'EN')
        self.assertEqual(p.currency, 'USD')

        logger.debug('Test provider put completed successfully')

class ServiceAreaViewSetTests(APITestCase):
    serviceAreaId = ''
    def add_test_serviceArea(self):
        """
        Adds a test serviceArea into the database
        """
        logger.debug('Adding a new serviceArea into database')
        jsonInfo = {
            "type": "Polygon",
            "coordinates": [
                [100.0, 0.0], [101.0, 0.0], [101.0, 1.0],
               [100.0, 1.0], [100.0, 0.0] 
            ],
            "provider":"provider1"
        }
        p = ServiceAreaModel( name='servicearea1', 
                    price=111,
                    geoJson=jsonInfo
        )
        p.save()
        self.serviceAreaId = p.id
        logger.debug('Successfully added test serviceArea into the database')

    def test_list_serviceAreas(self):
        """
        Test to list all the serviceAreas in the list
        """
        logger.debug('Starting test list serviceAreas')

        self.add_test_serviceArea()

        url = 'http://localhost:8000/api/servicearea/'

        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.get(url, format='json')
        json = response.json()

        logger.debug('Testing status code response: %s, code: %d'%(response, response.status_code))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        logger.debug('Testing result count')
        self.assertEqual(len(json['serviceArea']), 1)

    def test_create_serviceArea(self):
        """
        Tests creating a new serviceArea object
        """
        logger.debug('Starting test create serviceArea')
        url = 'http://localhost:8000/api/servicearea/'
        data = {
            'name' :'serviceArea1', 
            'price' : 111,
            'geoJson': {
                "type": "Polygon",
                "coordinates": [
                    [100.0, 0.0], [101.0, 0.0], [101.0, 1.0],
                    [100.0, 1.0], [100.0, 0.0] 
                ],
                "provider":"provider1"
            }
        }

        logger.debug('Sending TEST data to url: %s, data: %s'%(url, data))
        response = self.client.post(url, data, format='json')
   
        logger.debug('Testing status code response: %s, code: %d'%(response, response.status_code))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        logger.debug('Testing serviceArea count to make sure object was successfully added')
        self.assertEqual(ServiceAreaModel.objects.count(), 1)

        logger.debug('Testing new serviceArea object details')
        p = ServiceAreaModel.objects.get()
        self.assertEqual(p.name, 'serviceArea1')
        self.assertEqual(p.price, 111)
        self.assertEqual(p.geoJson, {
                "type": "Polygon",
                "coordinates": [
                    [100.0, 0.0], [101.0, 0.0], [101.0, 1.0],
                    [100.0, 1.0], [100.0, 0.0] 
                ],
                "provider":"provider1"
            })
        

        logger.debug('Test serviceArea create completed successfully')

    def test_delete_serviceAreas(self):
        """
        Test to see if deleting works
        """
        logger.debug('Starting test delete serviceAreas')

        self.add_test_serviceArea()

        url = 'http://localhost:8000/api/servicearea/%s'%self.serviceAreaId
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.delete(url, format='json')

        logger.debug('Testing to see if status code is correct')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_put_serviceAreas(self):
        """
        Test to see if put works
        """
        logger.debug('Starting test put serviceAreas')

        self.add_test_serviceArea()

        url = 'http://localhost:8000/api/servicearea/%s'%self.serviceAreaId
        logger.debug('Sending TEST data to url: %s'%url)
        data = {
            'name' :'serviceArea1', 
            'price' : 111,
            'geoJson': {
                "type": "Polygon",
                "coordinates": [
                    [100.0, 0.0], [101.0, 0.0], [101.0, 1.0],
                    [100.0, 1.0], [100.0, 0.0] 
                ],
                "provider":"provider1"
            }
        }
        
        response = self.client.patch(url, data, format='json')
        
        logger.debug('Testing to see if status code is correct')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        logger.debug('Testing modified serviceArea object details')
        p = ServiceAreaModel.objects.get()
        self.assertEqual(p.name, 'serviceArea1')
        self.assertEqual(p.price, 111)
        self.assertEqual(p.geoJson, {
                "type": "Polygon",
                "coordinates": [
                    [100.0, 0.0], [101.0, 0.0], [101.0, 1.0],
                    [100.0, 1.0], [100.0, 0.0] 
                ],
                "provider":"provider1"
            })

        logger.debug('Test serviceArea put completed successfully')