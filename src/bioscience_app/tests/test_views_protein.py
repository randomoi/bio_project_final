from django.test import TestCase, Client
from django.urls import reverse
from bioscience_app.models import Protein, Organism, Domain, Pfam, DomainAssignment
from ..forms import NewProteinForm 
from django.core.exceptions import ValidationError
from ..views_protein import data_validation, if_data_exists

# START: I wrote the code based on documentation and references. Important links were included in the comments. 
# Please review links below and short commentary in readme.txt. Thank you.

# https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing
class ViewsProteinTests(TestCase):
    def setUp(self):
        # creating test client
        self.client = Client()

    def test_new_protein_form_page_code_GET(self):
        # send GET request 
        response = self.client.get(reverse('new_protein_form_page'))

        # testing if response is 200
        self.assertEqual(response.status_code, 200)

    def test_new_protein_form_page_template_GET(self):
        # send GET request 
        response = self.client.get(reverse('new_protein_form_page'))

        # testing if correct template used
        self.assertTemplateUsed(response, 'bioscience_app/create_new_protein.html')

    def test_new_protein_form_page_POST(self):
        # data for the POST request
        data = {
            'protein_id': 'some protein id',
            'sequence': 'some sequence',
            'organism': {
                'taxa_id': 'some taxa',
                'clade': 'some clade',
                'genus': 'some genus',
                'species': 'some species'
            },
            'length': 123,
            'domains': [{
                'pfam_id': {
                    'domain_id': 'some domain id',
                    'domain_description': 'some description'
                },
                'description': 'some description',
                'start': 1,
                'end': 2
            }]
        }

        # testing if request is POST
        response = self.client.post(reverse('new_protein_form_page'), data)


class ProteinModelValidationTests(TestCase):
    def test_data_validation(self):
        # data for the validation
        data = {
            'protein_id': 'some protein id',
            'sequence': 'some sequence',
            'organism': {
                'taxa_id': 'some taxa',
                'clade': 'some clade',
                'genus': 'some genus',
                'species': 'some species'
            },
            'length': 123,
            'domains': [{
                'pfam_id': {
                    'domain_id': 'some domain id',
                    'domain_description': 'some description'
                },
                'description': 'some description',
                'start': 1,
                'end': 2
            }]
        }

        # validate that the data doesnt raise errors
        data_validation(data)  

    def test_if_data_exists(self):
        # data for the validation
        data = {
            'protein_id': 'some protein id',
            'sequence': 'some sequence',
            'organism': {
                'taxa_id': 123,
                'clade': 'some clade',
                'genus': 'some genus',
                'species': 'some species'
            },
            'length': 123,
            'domains': [{
                'domain_id': 'some domain id',
                'domain_description': 'some description',
                'start': 1,
                'end': 2
            }]
        }

        # create Organism
        organism = Organism.objects.create(
            taxa_id=123,
            clade='some clade',
            genus='some genus',
            species='some species'
        )
        
        # create Protein
        protein = Protein.objects.create(
            protein_id='some protein id',
            sequence='some sequence',
            organism=organism,
            length=123
        )
        
        # create domain
        domain = Domain.objects.create(
            domain_description='some description'
        )

        # create Domain Assignment 
        domain_assignment = DomainAssignment.objects.create(
            protein=protein,
            start=1,
            end=2,
            domain=domain  # assign Domain instance instead of Pfam
        )

        # check if_data_exists 
        with self.assertRaises(ValidationError):
            if_data_exists(data)  # must raise a ValidationError as data already exists

# END: I wrote the code based on documentation and references. Important links were included in the comments. 
# Please review links below and short commentary in readme.txt. Thank you.