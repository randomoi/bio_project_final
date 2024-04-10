from django.test import TestCase, Client
from django.urls import reverse

# START: I wrote the code based on documentation and references. Important links were included in the comments. 
# Please review links below and short commentary in readme.txt. Thank you.

# https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing
class TestSPAIndexViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.spa_url = reverse('spa')  
        self.index_url = reverse('index')  
    
    # testing if response code is 200
    def test_spa_code_GET(self):
        response = self.client.get(self.spa_url)

        self.assertEqual(response.status_code, 200)
    
    # testing if correct template used
    def test_spa_template_GET(self):
        response = self.client.get(self.spa_url)

        self.assertTemplateUsed(response, 'bioscience_app/spa.html')

    # testing if response code is 200
    def test_index_code_view_GET(self):
        response = self.client.get(self.index_url)

        self.assertEqual(response.status_code, 200)
    
    # testing if correct template used
    def test_index_template_view_GET(self):
        response = self.client.get(self.index_url)

        self.assertTemplateUsed(response, 'bioscience_app/spa.html')

# END: I wrote the code based on documentation and references. Important links were included in the comments. 
# Please review links below and short commentary in readme.txt. Thank you.