from rest_framework.test import APITestCase
from django.urls import reverse
import json
from .factories import FactoryForProtein, FactoryForOrganism, FactoryForDomain, FactoryForPfam, FactoryForDomainAssignment
from bioscience_app.models import Protein, DomainAssignment
from django.test import TestCase, Client

# START: I wrote the code based on documentation and references. Important links were included in the comments. 
# Please review links below and short commentary in readme.txt. Thank you.

# https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing

class ProteinAPITest(APITestCase):
    def setUp(self):
        # create protein objects with FactoryForProtein 
        self.protein1 = FactoryForProtein.create(pk=1, protein_id="protein1")
        self.protein2 = FactoryForProtein.create(pk=2, protein_id="protein2")
        # set a good URL using protein1
        self.good_url = reverse('protein-detail', kwargs={'protein_id': self.protein1.protein_id})
        # set a delete URL using protein2 
        self.delete_url = reverse('protein-detail', kwargs={'protein_id': self.protein2.protein_id})
        # set a bad URL for 404 testing error
        self.bad_url = "/api/protein/nonexistent_protein/"

    # test protein detail url returns 200 
    def test_RetrieveProteinByIDViewReturnsSuccess(self):
        # GET request to good url
        response = self.client.get(self.good_url, format='json')
        # render response
        response.render()
        # test if response is 200
        self.assertEqual(response.status_code, 200)
       
        # test if valid protein ID is returned
    def test_RetrieveProteinByIDView_with_data_ReturnsSuccess(self):
        # GET request to good url
        response = self.client.get(self.good_url, format='json')
        # render response
        response.render()
        # load as JSON
        data = json.loads(response.content)
        # validate response data has correct protein_id
        self.assertTrue('protein_id' in data)

    # test protein detail for invalid protein id and response returns 404 error 
    def test_RetrieveProteinByIDViewReturnFailOnBadPk(self):
        # GET request to bad url
        response = self.client.get(self.bad_url, format='json')
        # validate response is 404
        self.assertEqual(response.status_code, 404)

    # tear down test case by deleting objects and resetting sequence
    def tearDown(self):
        Protein.objects.all().delete()
        FactoryForProtein.reset_sequence(0)


class ListProteinByTaxaViewTest(APITestCase):
    def setUp(self):
        # create organism using FactoryForOrganism
        self.organism = FactoryForOrganism.create()
        # create protein object using FactoryForProtein and assign it to organism 
        self.protein = FactoryForProtein.create(organism=self.organism)
        # create good URL 
        self.good_url = reverse('protein_by_taxa', args=[self.organism.taxa_id])
       
    # testing if response is 200 
    def test_get_proteins_by_taxa_code(self):
        # GET request 
        response = self.client.get(self.good_url, format='json')
        # validate response is 200
        self.assertEqual(response.status_code, 200)

    # testing if returns a list
    def test_get_proteins_by_taxa_list(self):
        # GET request 
        response = self.client.get(self.good_url, format='json')
        # load  JSON data
        data = json.loads(response.content)
        # validate response is a list
        self.assertTrue(isinstance(data, list), "Response data is a list.")

    # testing response is not empty  
    def test_get_proteins_by_taxa_is_not_empty(self):
        # GET request t
        response = self.client.get(self.good_url, format='json')
        # load response as JSON data
        data = json.loads(response.content)
        # validate response is not empty
        self.assertTrue(data, "Response data should not be empty")

    # test 1st element has a protein_id
    def test_get_proteins_by_taxa_1st_element_is_protein_id(self):
        # GET request 
        response = self.client.get(self.good_url, format='json')
        # load data as JSON
        data = json.loads(response.content)
        # validate 1st element has a 'protein_id'
        self.assertTrue('protein_id' in data[0], "Response data has 1st element as protein_id.")

    # testing returns empty list without data 
    def test_get_proteins_by_taxa_returns_empty_list_no_data(self):
        # delete all proteins 
        Protein.objects.filter(organism=self.organism).delete()
        # GET request 
        response = self.client.get(self.good_url, format='json')
        # load data as JSON
        data = json.loads(response.content)
        # validate response data is empty list
        self.assertEqual(len(data), 0, "Response data is an empty list without proteins for specified taxa.")
        
    # tear down by deleting objects
    def tearDown(self):
        self.organism.delete()
        self.protein.delete()


class ListDomainByTaxaViewTest(APITestCase):
    def setUp(self):
        self.organism = FactoryForOrganism.create()
        self.protein = FactoryForProtein.create(organism=self.organism)
        self.domain = FactoryForDomain.create()
        self.domain_assignment = FactoryForDomainAssignment.create(protein=self.protein, domain=self.domain)
        self.good_url = reverse('domain_by_taxa', args=[self.organism.taxa_id])

   # test response is 200 
    def test_get_domains_by_taxa_code_200(self):
        response = self.client.get(self.good_url, format='json')
        self.assertEqual(response.status_code, 200)
 
    # test response is list of data 
    def test_get_domains_by_taxa_is_list(self):
        response = self.client.get(self.good_url, format='json')
        data = response.json()
        self.assertTrue(isinstance(data, list), "Response is a list of data.")

    # test response data is not empty
    def test_get_domains_by_taxa_is_not_empty(self):
        response = self.client.get(self.good_url, format='json')
        data = response.json()
        self.assertTrue(len(data) >= 1, "Response data is not empty.")

    # test 1st element is data with pfam_id
    def test_get_domains_by_taxa_1st_element_contains_pfam_id(self):
        response = self.client.get(self.good_url, format='json')
        data = response.json()
        self.assertTrue('pfam_id' in data[0], "First element should have 'pfam_id'")

    # testing for an empty list 
    def test_get_domains_by_taxa_no_data_list_is_empty(self):
        DomainAssignment.objects.filter(protein=self.protein).delete()
        response = self.client.get(self.good_url, format='json')
        data = response.json()
        self.assertEqual(len(data), 0, "Response is an empty list.")

    # delete onjects
    def tearDown(self):
        self.organism.delete()
        self.protein.delete()
        self.domain.delete()
        self.domain_assignment.delete()


class CreateNewProteinViewTest(APITestCase):
    def setUp(self):
        self.protein = FactoryForProtein.create()
        self.url = reverse('protein-list')

    def test_get_protein_list_results(self):
        # good URL
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertTrue('results' in data)

        # test 1st result has a protein_id
        self.assertTrue('protein_id' in data['results'][0])

        # test bad URL
        response = self.client.get(reverse('protein-list') + 'bad/', format='json')

        # test for response with 404
        self.assertEqual(response.status_code, 404)
        
    # test for protein when it doesnt exists
    def test_create_new_protein_does_not_exists(self):
            protein_id = 'new_protein_id_123'
            data = {
                'protein_id': protein_id,
                'sequence': 'TYJBJHLKHKHOHIIGFYU',
                'length': 123,
                'organism': FactoryForOrganism.create().taxa_id,
                'id_custom': 12345,
            }

            # test that protein does not exist (before it's created)
            self.assertFalse(Protein.objects.filter(protein_id=protein_id).exists())

    def test_create_new_protein_missing_field(self):
        data = {
            'protein_id': 'new_protein_id_123',
            'sequence': 'TYJBJHLKHKHOHIIGFYU',
            'length': 123,
            'organism': FactoryForOrganism.create().taxa_id,
            # id_custom field is not there
        }

        # test for 404 response when a required field is missing
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, 400)

        # validate that protein was not created
        self.assertFalse(Protein.objects.filter(protein_id='new_protein').exists())

    # tear down object
    def tearDown(self):
        self.protein.delete()



class CreateNewProteinViewTest2(APITestCase):
    def setUp(self):
        # create a Protein 
        self.protein = FactoryForProtein.create()  
        # create URL 
        self.url = reverse('protein-list') 

    def test_get_protein_list_code_200(self):
        # GET request
        response = self.client.get(self.url, format='json')  
        # test response is 200
        self.assertEqual(response.status_code, 200)  

    def test_get_protein_list_has_results(self):
        # GET request 
        response = self.client.get(self.url, format='json')  
        data = response.json()  
        # test response has results
        self.assertTrue('results' in data) 

    def test_get_protein_list_first_result_contains_protein_id(self):
        # GET request 
        response = self.client.get(self.url, format='json')  
        data = response.json()  
        # test 1st result has protein_id
        self.assertTrue('protein_id' in data['results'][0])  

    def test_get_protein_list_with_bad_url_code_404(self):
        # GET request to bad URL
        response = self.client.get(reverse('protein-list') + 'bad/', format='json')  
        # test 404 response 
        self.assertEqual(response.status_code, 404) 

    def test_create_new_protein_does_not_exist(self):
        protein_id = 'new_protein_id_123'
        data = {
            'protein_id': protein_id,
            'sequence': 'TYJBJHLKHKHOHIIGFYU',
            'length': 123,
            'organism': FactoryForOrganism.create().taxa_id,
            'id_custom': 1234567,
        }
        self.assertFalse(Protein.objects.filter(protein_id=protein_id).exists())  # test protein doesnt exist

    def test_create_new_protein_missing_field_code_400(self):
        data = {
            'protein_id': 'new_protein_id_123',
            'sequence': 'TYJBJHLKHKHOHIIGFYU',
            'length': 123,
            'organism': FactoryForOrganism.create().taxa_id,
        }
        # POST request 
        response = self.client.post(self.url, data=data, format='json')  
        # test for 404 response 
        self.assertEqual(response.status_code, 400)  

    def test_create_new_protein_missing_field_does_not_create_new_protein(self):
        data = {
            'protein_id': 'new_protein_id_123',
            'sequence': 'TYJBJHLKHKHOHIIGFYU',
            'length': 123,
            'organism': FactoryForOrganism.create().taxa_id,
        }
        # POST request 
        response = self.client.post(self.url, data=data, format='json')  
        # test protein wasnt created
        self.assertFalse(Protein.objects.filter(protein_id='new_protein').exists())  

    # tear down object
    def tearDown(self):
        self.protein.delete()  



class RetrieveProteinByIDViewTest(APITestCase):
    def setUp(self):
        # create object
        self.protein = FactoryForProtein.create()  
        # good URL 
        self.url = reverse('protein-detail', args=[self.protein.protein_id]) 

    def test_get_protein_detail_code_200(self):
        # GET request 
        response = self.client.get(self.url, format='json')  
        # test response is 200  
        self.assertEqual(response.status_code, 200)  

    def test_get_protein_detail_contains_correct_protein_id(self):
        # GET request 
        response = self.client.get(self.url, format='json')  
        data = response.json()  
        # test response has correct protein id
        self.assertEqual(data['protein_id'], self.protein.protein_id) 

# tear down object  
    def tearDown(self):
        self.protein.delete() 



class RetrievePfamDetailsViewTest(APITestCase):
    def setUp(self):
        # create object 
        self.pfam = FactoryForPfam.create() 
        # good URL 
        self.url = reverse('pfam-domain-detail', args=[self.pfam.domain_id])  

    def test_get_pfam_detail_code_200(self):
        # GET request
        response = self.client.get(self.url, format='json')   
        # test response is 200
        self.assertEqual(response.status_code, 200)  

    def test_get_pfam_detail_contains_correct_domain_id(self):
        # GET request 
        response = self.client.get(self.url, format='json')  
        data = response.json()  
        # test response has correct domain id
        self.assertEqual(data['domain_id'], self.pfam.domain_id) 

    # tear down object
    def tearDown(self):
        self.pfam.delete()  


class CoverageViewTest(APITestCase):
    def setUp(self):
        # create objects
        self.protein = FactoryForProtein.create()  
        self.domain = FactoryForDomain.create()  
        # assign Domain to Protein 
        self.domain_assignment = FactoryForDomainAssignment.create(protein=self.protein, domain=self.domain, start=1, end=self.protein.length) 
        # good URL  with valid protein id
        self.good_url = reverse('coverage', args=[self.protein.protein_id])  
        # bad a URL with not valid protein id
        self.bad_url = reverse('coverage', args=['invalid_protein_id'])  

    def test_get_coverage_code_200(self):
        # GET request 
        response = self.client.get(self.good_url, format='json') 
        # test response is 200
        self.assertEqual(response.status_code, 200)  

    def test_get_coverage_contains_valid_coverage(self):
        # GET request 
        response = self.client.get(self.good_url, format='json')  
        data = response.json()  
        # test coverage is 100% rounded to 2 decimals
        self.assertAlmostEqual(data['coverage'], 1.0, places=2)  

    def test_get_coverage_for_invalid_protein_id_code_404(self):
        response = self.client.get(self.bad_url, format='json')  # GET request 
        # test response is 404
        self.assertEqual(response.status_code, 404) 

    # tear down objects         
    def tearDown(self):
        self.protein.delete()  
        self.domain.delete()  
        self.domain_assignment.delete()  


class SwaggerReDocTests(TestCase):
    def setUp(self):
        self.client = Client()

    # test response code is 200
    def test_swagger_code_response(self):
        response = self.client.get('/api/swagger/')
        self.assertEqual(response.status_code, 200)

    # test that swagger is displayed
    def test_swagger_view_response(self):
        response = self.client.get('/api/swagger/')
        self.assertContains(response, 'swagger')  

    # test response code is 200
    def test_redoc_code_response(self):
        response = self.client.get('/api/redoc/')
        self.assertEqual(response.status_code, 200)

    # test that reDoc is displayed
    def test_redoc_ui_response(self):
        response = self.client.get('/api/redoc/')
        self.assertContains(response, 'redoc')  

    # test response code is 200
    def test_django_login_code(self):
        response = self.client.get('/admin/login/?next=/api/swagger/')
        self.assertEqual(response.status_code, 200)
       
    # test that login is displayed
    def test_django_login_ui_view(self):
        response = self.client.get('/admin/login/?next=/api/swagger/')
        self.assertContains(response, 'Log in')  

# END: I wrote the code based on documentation and references. Important links were included in the comments. 
# Please review links below and short commentary in readme.txt. Thank you.