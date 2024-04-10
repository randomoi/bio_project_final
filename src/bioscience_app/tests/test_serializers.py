from django.test import TestCase
import json
from django.urls import reverse
from django.urls import reverse_lazy
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
import factory
from bioscience_app.models import Organism, Protein, Pfam, Domain, DomainAssignment
from bioscience_app.serializers import SerializerForOrganism, SerializerForPfam, SerializerForDomainByTaxa, SerializerForDomainAssignment, SerializerForProtein, SerializerForProteinByTaxa
from .factories import FactoryForOrganism, FactoryForProtein, FactoryForPfam, FactoryForDomain, FactoryForDomainAssignment

# START: I wrote the code based on documentation and references. 
# Please review short commentary in readme.txt. Thank you.

# serializers have been with two approaches 
# 1) directly creating objects in the test methods using Django's built-in ORM
# 2) using factory boy with factories created in factories.py
# 3) I've written failing tests during testing process. Initially I used TDD, but the project became too large to handle in a small period of time, therefore, I've moved on to simplified development process.
##########################################################
# 1) TESTS using Django's built-in ORM

class SerializerForOrganismTestCase(TestCase):
    def setUp(self):
        # create object
        self.organism = Organism.objects.create(taxa_id=1, clade='Clade123', genus='Genus123', species='Species123')
        # create serializer 
        self.serializer = SerializerForOrganism(instance=self.organism)

    def test_expected_output(self):
        # expected serialized output 
        expected_output = {
            'id': 1,
            'taxa_id': 1,
            'clade': 'Clade123',
            'genus': 'Genus123',
            'species': 'Species123'
        }
        # validate that serialized output = expected output
        self.assertEqual(self.serializer.data, expected_output)


class SerializerForPfamTestCase(TestCase):
    def setUp(self):
        # create object 
        self.pfam = Pfam.objects.create(domain_id='Domain123', domain_description='Some Description')
        # create a serializer 
        self.serializer = SerializerForPfam(instance=self.pfam)

    def test_expected_output(self):
         # expected serialized output 
        expected_output = {
            'domain_id': 'Domain123',
            'domain_description': 'Some Description'
        }
        # validate that serialized output = expected output
        self.assertEqual(self.serializer.data, expected_output)


class SerializerForDomainAssignmentTestCase(TestCase):
    def setUp(self):
        # create objects
        self.pfam = Pfam.objects.create(domain_id='Domain123', domain_description='Some Description')
        self.organism = Organism.objects.create(taxa_id=1, clade='Clade123', genus='Genus123', species='Species123')
        self.protein = Protein.objects.create(protein_id='Protein ID123', sequence='Sequence123', length=100, organism=self.organism)
        self.domain = Domain.objects.create(domain_description='Some Description', pfam=self.pfam)
        self.domain_assignment = DomainAssignment.objects.create(protein=self.protein, domain=self.domain, start=1, end=75)

    def test_expected_output_domain_assignment(self):
        # get serialized data 
        data = SerializerForDomainAssignment(instance=self.domain_assignment).data
        # expected serialized data 
        expected_data = {
            'pfam_id': {'domain_id': 'Domain123', 'domain_description': 'Some Description'},
            'description': 'Some Description',  
            'start': 1,
            'stop': 75,
        }
        # validate that serialized output = expected output
        self.assertEqual(data, expected_data)

    def test_expected_output_pfam(self):
        # get serialized data 
        data = SerializerForPfam(instance=self.pfam).data
        # expected serialized data 
        expected_data = {
            'domain_id': 'Domain123',
            'domain_description': 'Some Description',
        }
        # validate that serialized output = expected output
        self.assertEqual(data, expected_data)


class SerializerForProteinByTaxaTestCase(TestCase):
    def setUp(self):
         # create objects
        self.organism = Organism.objects.create(taxa_id=1, clade='Clade123', genus='Genus123', species='Species123')
        self.protein = Protein.objects.create(protein_id='Protein ID123', sequence='Sequence123', length=10, organism=self.organism, id_custom=1)

    def test_expected_output(self):
        # get serialized data 
        data = SerializerForProteinByTaxa(instance=self.protein).data
        # expected serialized data 
        expected_data = {
            'id': 1,  
            'protein_id': 'Protein ID123',
        }
        # validate that serialized output = expected output
        self.assertEqual(data, expected_data)

class SerializerForProteinTestCase(TestCase):
    def setUp(self):
        # create objects
        self.organism = Organism.objects.create(
            taxa_id=1234,
            clade='Clade123',
            genus='Genus123',
            species='Species123'
        )
        self.protein = Protein.objects.create(
            protein_id='Protein ID123',
            sequence='Protein Sequence32152',
            organism=self.organism
        )
        self.pfam = Pfam.objects.create(
            domain_id='Domain123',
            domain_description='Some Description'
        )
        self.domain = Domain.objects.create(
            pfam=self.pfam,
            domain_description='Some Domain'  
        )
        self.domain_assignment = DomainAssignment.objects.create(
            start=1,
            end=5,
            protein=self.protein,
            domain=self.domain
        )

    def test_expected_output(self):
        # get serialized data 
        data = SerializerForProtein(instance=self.protein)
        # convert to regular dictionary
        convert_data_to_regular_dict = json.loads(json.dumps(data.data))
        # expected serialized data 
        expected_output = {
            'protein_id': 'Protein ID123',
            'sequence': 'Protein Sequence32152',
            'length': 0,  
            'taxonomy': {
                'id': 1,
                'taxa_id': 1234,
                'clade': 'Clade123',
                'genus': 'Genus123',
                'species': 'Species123'
            },
            'domains': [
                {
                    'pfam_id': {
                        'domain_id': 'Domain123',
                        'domain_description': 'Some Description'
                    },
                    'description': 'Some Description',  
                    'start': 1,
                    'stop': 5
                }
            ]
        }
        # validate that serialized output = Dict
        self.assertDictEqual(convert_data_to_regular_dict, expected_output)


class ProteinWithoutDomainsSerializerTestCase(TestCase):
    def setUp(self):
        # create objects
        self.organism = Organism.objects.create(
            taxa_id=5678,
            clade='Clade321',
            genus='Genus321',
            species='Species321'
        )
        self.protein_without_domains = Protein.objects.create(
            protein_id='Protein ID321',
            sequence='Protein Sequence321',
            organism=self.organism
        )

    
    def test_output_without_domains(self):
        # get serialized data 
        data = SerializerForProtein(instance=self.protein_without_domains)
        # convert to regular dictionary
        convert_data_to_regular_dict = json.loads(json.dumps(data.data))
        # expected serialized data 
        expected_output = {
            'protein_id': 'Protein ID321',
            'sequence': 'Protein Sequence321',
            'length': 0,  
            'taxonomy': {
                'id': 1,
                'taxa_id': 5678,
                'clade': 'Clade321',
                'genus': 'Genus321',
                'species': 'Species321'
            },
            'domains': []  # empty
        }
        # validate that serialized output = expected output
        self.assertDictEqual(convert_data_to_regular_dict, expected_output)

class SerializerForDomainByTaxaTestCase(TestCase):
    def setUp(self):
       # create objects
        self.pfam = Pfam.objects.create(
            domain_id='Domain123',
            domain_description='Some Description'
        )
      
        self.domain = Domain.objects.create(pfam=self.pfam)

        # create serializer 
        self.serializer = SerializerForDomainByTaxa(instance=self.domain)


    def test_expected_output(self):
        # expected serialized data 
        expected_output = {
            'id': self.domain.id,
            'pfam_id': {
                'domain_id': 'Domain123',
                'domain_description': 'Some Description'
            }
        }
       # validate that serialized output != expected output
        self.assertEqual(self.serializer.data, expected_output)

####################### END TESTS using Django's built-in ORM



#################################################
### 2) TESTS using Factory Boy

class SerializerForOrganismWithFactoryTest(TestCase):
    def setUp(self):
        # create object
        self.organism = FactoryForOrganism(taxa_id=1, clade='Clade123', genus='Genus123', species='Species123')
        # create serializer for object
        self.serializer = SerializerForOrganism(instance=self.organism)

    def test_expect_output(self):
        # expected output
        expected_output = {
            'id': 1,
            'taxa_id': 1,
            'clade': 'Clade123',
            'genus': 'Genus123',
            'species': 'Species123'
        }
        # validate that serialized output = expected output
        self.assertEqual(self.serializer.data, expected_output)



class SerializerForPfamWithFactoryTest(TestCase):
    def setUp(self):
         # create object
        self.pfam = FactoryForPfam(domain_id='Domain123', domain_description='Some Description')
        # create serializer for object
        self.serializer = SerializerForPfam(instance=self.pfam)

    def test_expected_output(self):
        # expected output
        expected_output = {
            'domain_id': 'Domain123',
            'domain_description': 'Some Description'
        }
         # validate that serialized output = expected output
        self.assertEqual(self.serializer.data, expected_output)


class SerializerForPfamWithFactoryTest(TestCase):
    def setUp(self):
        # create object
        self.pfam = FactoryForPfam()

    def test_expected_output(self):
        # get data
        data = SerializerForPfam(instance=self.pfam).data
        # expected output
        expected_output = {
            'domain_id': self.pfam.domain_id,
            'domain_description': self.pfam.domain_description
        }
        # validate that serialized output = expected output
        self.assertEqual(data, expected_output)


class SerializerForProteinByTaxaWithFactoryTest(TestCase):
    def setUp(self):
        # create objects
        self.organism = FactoryForOrganism()
        self.protein = FactoryForProtein(organism=self.organism, id_custom=1)

    def test_expected_output(self):
        # Create a serializer for the Protein object
        data = SerializerForProteinByTaxa(instance=self.protein).data
        # expected output
        expected_output = {
            'id': self.protein.id_custom, 
            'protein_id': self.protein.protein_id,
        }
         # validate that serialized output = expected output
        self.assertEqual(data, expected_output)

############# END TESTS using Factory Boy


#################################################
## 3) FAILING TESTS

# ## FAILING - Reason: taxa_id field is a string, not integer
# class SerializerForOrganismFailingTestCase(TestCase):
#     def setUp(self):
#         self.organism = Organism.objects.create(taxa_id='Test Taxa ID', clade='Clade123', genus='Genus123', species='Species123')
#         self.serializer = SerializerForOrganism(instance=self.organism)

#     def test_expected_output_failing(self):
#         expected_output = {
#             'taxa_id': 1,
#             'clade': 'Clade123',
#             'genus': 'Genus123',
#             'species': 'Species123'
#         }
#         self.assertEqual(self.serializer.data, expected_output)


# ### FAILING -  assertion is not equal 
# class SerializerForPfamFailingTestCase(TestCase):
#     def setUp(self):
#         self.pfam = Pfam.objects.create(domain_id='Domain123', domain_description='Some Description')
#         self.serializer = SerializerForPfam(instance=self.pfam)

#     def test_expected_output_failing(self):
#         expected_output = {
#             'domain_id': 'Domain123',
#             'domain_description': 'Some Description'
#         }
#         self.assertNotEqual(self.serializer.data, expected_output)

# ### FAILING  -  not equal to the expected_output dictionary.
# class SerializerForDomainAssignmentFailingTestCase(TestCase):
#     def setUp(self):
#         self.pfam = Pfam.objects.create(domain_id='Domain123', domain_description='Some Description')
#         self.organism = Organism.objects.create(taxa_id=1, clade='Clade123', genus='Genus123', species='Species123')
#         self.protein = Protein.objects.create(protein_id='Protein ID123', sequence='Sequence123', length=100, organism=self.organism)
#         self.domain = Domain.objects.create(domain_description='Some Description', pfam=self.pfam)
#         self.domain_assignment = DomainAssignment.objects.create(protein=self.protein, domain=self.domain, start=1, end=75)

#     def test_expected_output_failing_domain_assignment(self):
#         data = SerializerForDomainAssignment(instance=self.domain_assignment).data
#         expected_output = {
#             'pfam_id': {'domain_id': 'Domain123', 'domain_description': 'Some Description'},
#             'description': 'Some Description',
#             'start': 1,
#             'stop': 75,
#         }
#         self.assertNotEqual(data, expected_output)

#     def test_expected_output_failing_pfam(self):
#         data = SerializerForPfam(instance=self.pfam).data
#         expected_data = {
#             'domain_id': 'Domain123',
#             'domain_description': 'Some Description',
#         }
#         self.assertEqual(data, expected_data)

# ### FAILING TEST - Reason: expected length =  length sequence 
# class SerializerForProteinFailingTestCase(TestCase):
#     def setUp(self):
#         self.organism = Organism.objects.create(
#             taxa_id=1234,
#             clade='Clade123',
#             genus='Genus123',
#             species='Species123'
#         )
#         self.protein = Protein.objects.create(
#             protein_id='Protein ID123',
#             sequence='Protein Sequence32152',
#             organism=self.organism
#         )

#     def test_expected_output_failing(self):
#         serializer = SerializerForProtein(instance=self.protein)
#         serializer_data = json.loads(json.dumps(serializer.data)) 
#         expected_output = {
#             'protein_id': 'Protein ID123',
#             'sequence': 'Protein Sequence32152',
#             'length': 22,  
#             'taxonomy': {
#                 'taxa_id': 1234,
#                 'clade': 'Clade123',
#                 'genus': 'Genus123',
#                 'species': 'Species123'
#             },
#             'domains': []  # empty
#         }
#         self.assertDictEqual(serializer_data, expected_output)




# #### FAILING - Reason: returns Ordered Dictionary 1= regular dictionary 
# class SerializerForProteinDataStructureFailingTestCase(TestCase):
#     def setUp(self):
#         self.organism = Organism.objects.create(
#             taxa_id=1234, # change to integer value
#             clade='Clade123',
#             genus='Genus123',
#             species='Species123'
#         )
#         self.protein = Protein.objects.create(
#             protein_id='Protein ID123',
#             sequence='Protein Sequence32152',
#             organism=self.organism,
#             length=108
#         )
#         self.pfam = Pfam.objects.create(
#             domain_id='Domain123',
#             domain_description='Some Description'
#         )
#         self.domain = Domain.objects.create(
#             pfam=self.pfam,
#             domain_description='Some Domain'
#         )
#         self.domain_assignment = DomainAssignment.objects.create(
#             start=1,
#             end=57,
#             protein=self.protein,
#             domain=self.domain
#         )

#     def test_expected_output_failing(self):
#         serializer = SerializerForProtein(instance=self.protein)
#         expected_output = {
#             'protein_id': 'Protein ID123',
#             'sequence': 'Protein Sequence32152',
#             'taxonomy': {
#                 'taxa_id': 1234, # change to integer value
#                 'clade': 'Clade123',
#                 'genus': 'Genus123',
#                 'species': 'Species123'
#             },
#             'length': 108,
#             'domains': [
#                 {
#                     'pfam_id': {
#                         'domain_id': 'Domain123',
#                         'domain_description': 'Some Description'
#                     },
#                     'description': 'Some Domain',
#                     'start': 1,
#                     'stop': 57
#                 }
#             ]
#         }
#         self.assertDictEqual(serializer.data, expected_output)

# ### FAILING 
# class SerializerForDomainByTaxaFailingTestCase(TestCase):
#     def setUp(self):
#         self.pfam = Pfam.objects.create(
#             domain_id='Domain123',
#             domain_description='Some Description'
#         )
#         self.domain = Domain.objects.create(
#             pfam=self.pfam,
#         )
#         self.organism = Organism.objects.create(
#             taxa_id=1,
#             clade='Clade123',
#             genus='Genus123',
#             species='Species123'
#         )
#         self.protein = Protein.objects.create(
#             protein_id='Protein ID123',
#             sequence='Protein Sequence32152',
#             organism=self.organism,
#             length=109
#         )
#         self.domain_assignment = DomainAssignment.objects.create(
#             domain=self.domain,
#             protein=self.protein,
#             start=10,
#             end=22
#         )
#         self.serializer = SerializerForDomainByTaxa(instance=self.domain_assignment)

#     def test_expected_output_failing(self):
#         expected_output = {
#             'id': self.domain_assignment.id,
#             'pfam_id': {
#                 'domain_id': 'Domain123',
#                 'domain_description': 'Some Description'
#             }
#         }

#         self.assertEqual(self.serializer.data, expected_output)

# ########### END Failing tests

# END: I wrote the code based on documentation and references. 
# Please review short commentary in readme.txt. Thank you.