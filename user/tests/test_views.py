import os
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
import json

class CSVUploadAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        base_dir = os.path.dirname(__file__)  # Get the directory of this test file
        self.valid_csv_path = os.path.join(base_dir, 'test_files', 'valid_csv.csv')
        self.invalid_csv_path = os.path.join(base_dir, 'test_files', 'invalid_csv.csv')
        self.response_file = 'response_output.json'

    def tearDown(self):
        # Clean up the response file after each test
        if os.path.exists(self.response_file):
            os.remove(self.response_file)

    def test_valid_csv_upload(self):
        with open(self.valid_csv_path, 'rb') as valid_csv:
            response = self.client.post('/upload/', {'file': valid_csv}, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn('message', response.json())
            self.assertTrue(os.path.exists(self.response_file))

    def test_invalid_csv_upload(self):
        with open(self.invalid_csv_path, 'rb') as invalid_csv:
            response = self.client.post('/upload/', {'file': invalid_csv}, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn('message', response.json())
            self.assertTrue(os.path.exists(self.response_file))
        
        # Verify the content of the JSON file
        with open(self.response_file, 'r') as json_file:
            response_data = json.load(json_file)
            self.assertIn('records_rejected', response_data)
            self.assertGreater(response_data['records_rejected'], 0)
 

# from django.test import TestCase
# from django.urls import reverse
# from rest_framework.test import APIClient
# from user.models import User
# import io
# from django.core.files.uploadedfile import SimpleUploadedFile

# class CSVUploadAPITest(TestCase):
#     def setUp(self):
#         self.client = APIClient()

#     def test_valid_csv_upload(self):
#         csv_content = """name,email,age
#         John Doe,john@example.com,25
#         Jane Doe,jane@example.com,30
#         """
#         file = SimpleUploadedFile('test.csv', csv_content.encode('utf-8'), content_type='text/csv')
#         response = self.client.post(reverse('csv-upload'), {'file': file})
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(User.objects.count(), 2)
    
#     def test_invalid_csv_upload(self):
#         csv_content = """name,email,age
#         Invalid User,invalidemail,130
#         """
#         file = SimpleUploadedFile('test.csv', csv_content.encode('utf-8'), content_type='text/csv')
#         response = self.client.post(reverse('csv-upload'), {'file': file})
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(User.objects.count(), 0)
#         self.assertIn('records_rejected', response.json())
