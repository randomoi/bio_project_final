from django.test import TestCase
import json
from django.urls import reverse, reverse_lazy
from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory, APITestCase
import factory
from bioscience_app.models import Organism, Protein, Pfam, Domain, DomainAssignment
from .factories import FactoryForOrganism, FactoryForProtein, FactoryForPfam, FactoryForDomain, FactoryForDomainAssignment
from django.db.utils import IntegrityError

# START: I wrote the code based on documentation and references. Important links were included in the comments. 
# Please review links below and short commentary in readme.txt. Thank you.

# https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing

### models have been with two approaches 
## 1) directly creating objects in the test methods using Django's built-in ORM
## 2) using factory boy with factories created in factories.py
## 3) I've written failing tests during testing process. Initially I used TDD, but the project became too large to handle in a small period of time, therefore, I've moved on to simplified development process.
########################################################
### 1) TESTS using Django's built-in ORM

class OrganismModelPassingTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # create object
        Organism.objects.create(taxa_id=1, clade='Clade865', genus='Genus865', species='Species865')

    # test uniqueness
    def test_unique_together_organism(self):
        with self.assertRaises(Exception):
            Organism.objects.create(taxa_id=1, clade='Clade865', genus='Genus865', species='Species865')

    # test organism creation 
    def test_create_new_organism(self):
        # create object 
        organism = Organism.objects.create(taxa_id=2, clade='Clade865', genus='Genus865', species='Species865')
        # validate string has expected value
        self.assertEqual(str(organism), '2, Clade865, Genus865, Species865')
    

class ProteinModelPassingTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # create objects
        organism = Organism.objects.create(taxa_id=1, clade='Clade865', genus='Genus865', species='Species865')
        Protein.objects.create(protein_id='protein865', sequence='sequence865', length=18, organism=organism)

    # test expected output
    def test_exected_output_str_rep(self):
        protein = Protein.objects.get(protein_id='protein865')
        expected_output = 'protein865 (Organism: Genus865 Species865)'
        self.assertEqual(str(protein), expected_output)

     # test for initial value to be note empty
    def test_id_custom_field(self):
        protein = Protein.objects.get(protein_id='protein865')
        self.assertIsNone(protein.id_custom)


class DomainModelPassingTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # create objects
        pfam = Pfam.objects.create(domain_id='domain865', domain_description='description865')
        Domain.objects.create(domain_description='domain_description865', pfam=pfam)

    def test_fields_for_pfam_not_none(self):
        # get Domain object 
        domain = Domain.objects.get(domain_description='domain_description865')
        # validate Pfam object is not None
        self.assertIsNotNone(domain.pfam)

    def test_new_domain_description(self):
        # create objects
        pfam = Pfam.objects.create(domain_id='domain865_2', domain_description='description865_2')
        domain = Domain.objects.create(domain_description='domain_description865_2', pfam=pfam)
        
        # validate object has the correct description
        self.assertEqual(domain.domain_description, 'domain_description865_2')

class DomainAssignmentModelPassingTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # create objects
        organism = Organism.objects.create(taxa_id=1, clade='Clade865', genus='Genus865', species='Species865')
        protein = Protein.objects.create(protein_id='protein865', sequence='sequence865', length=18, organism=organism)
        pfam = Pfam.objects.create(domain_id='domain865', domain_description='description865')
        domain = Domain.objects.create(domain_description='domain_description865', pfam=pfam)
        DomainAssignment.objects.create(protein=protein, domain=domain, start=1, end=19)
    
    def test_unique_together_domain_assignment(self):
        with self.assertRaises(Exception):
            # get objects
            protein = Protein.objects.get(protein_id='protein865')
            domain = Domain.objects.get(domain_description='domain_description865')
            # create new Domain Assignment object with unique_together_domain_assignment
            DomainAssignment.objects.create(protein=protein, domain=domain, start=1, end=19)


class PfamModelPassingTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # create object 
        Pfam.objects.create(domain_id='domain865', domain_description='description865')

    # test "str" method returns the expected string 
    def test_expected_str_representation_pfam(self):
        pfam = Pfam.objects.get(domain_id='domain865')
        self.assertEqual(str(pfam), 'domain865: description865')

    # test "str" method returns expected string 
    def test_create_pfam_expected(self):
        # create object
        pfam = Pfam.objects.create(domain_id='domain865_2', domain_description='domain865_2')
        self.assertEqual(str(pfam), 'domain865_2: domain865_2')


class PfamModelPassingTest2(TestCase):
    def test_unique_together_domain_id(self):
        Pfam.objects.create(domain_id='domain865', domain_description='description865')
        with self.assertRaises(Exception):
            Pfam.objects.create(domain_id='domain865', domain_description='description865')

class ProteinListPassingTest(TestCase):
    def setUp(self):
        # test client
        self.client = APIClient()

        # create objects 
        self.organism = Organism.objects.create(
            taxa_id=1, clade='Clade865', genus="Genus865", species='species865'
        )

        self.protein_1 = Protein.objects.create(
            protein_id='protein865_1',
            sequence='sequence865',
            length=18,
            organism=self.organism,
        )
        self.protein_2 = Protein.objects.create(
            protein_id="protein865_2",
            sequence='sequence865',
            length=18,
            organism=self.organism,
        )

    # test response is 200
    def test_protein_list_view_status_code_200(self):
        response = self.client.get(reverse("protein-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # test response data length
    def test_expected_protein_list_view_data_length(self):
        response = self.client.get(reverse("protein-list"))
        self.assertEqual(len(response.data), 4)

    # test response is 200 for indicated taxa_id 
    def test_protein_list_view_with_taxa_id_status_code_200(self):
        url = reverse("protein_by_taxa", kwargs={"taxa_id": self.organism.taxa_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # test response data length for indicated taxa_id
    def test_protein_list_view_with_taxa_id_data_length(self):
        url = reverse("protein_by_taxa", kwargs={"taxa_id": self.organism.taxa_id})
        response = self.client.get(url)
        self.assertEqual(len(response.data), 2)

# ############### # END TESTS using Django's built-in ORM


# #####################################
###### 2) TESTS using Factory Boy

class OrganismModelWithFactoryPassingTest(TestCase):
    def test_unique_together_with_factory(self):
        # create object 
        organism = FactoryForOrganism(taxa_id=1, clade='Clade865', genus='Genus865', species='Species865')
        
        # try to create another object with the same values
        with self.assertRaises(Exception):
            organism(taxa_id=1, clade='Clade865', genus='Genus865', species='Species865')

    # test creation of a new object with indicated values 
    def test_create_organism_with_factory(self):
        organism = FactoryForOrganism(taxa_id=2, clade='Clade865', genus='Genus865', species='Species865')

        # validate string has expected output 
        self.assertEqual(str(organism), '2, Clade865, Genus865, Species865')


class ProteinModelWithFactoryPassingTest(TestCase):
    def setUp(self):
        # create object 
        self.protein = FactoryForProtein(id_custom=3839)

    # test "str" method returns expected output 
    def test_str_representation_with_factory(self):
        expected_output = f'{self.protein.protein_id} (Organism: {self.protein.organism.genus} {self.protein.organism.species})'
        self.assertEqual(str(self.protein), expected_output)

    # test sequence is string
    def test_sequence_field_with_factory(self):
        self.assertIsInstance(self.protein.sequence, str)

    # test length is integer
    def test_length_field_with_factory(self):
        self.assertIsInstance(self.protein.length, int)

    # test id_custom is not None
    def test_id_custom_field_with_factory(self):
        self.assertIsNotNone(self.protein.id_custom)



class PfamModelWithFactoryPassingTest(TestCase):
    def setUp(self):
        # create object 
        self.pfam = FactoryForPfam()

    # test string of object 
    def test_str_representation_with_factory(self):
        expected_output = f"{self.pfam.domain_id}: {self.pfam.domain_description}"
        self.assertEqual(str(self.pfam), expected_output)

    # test object failed to create with domain id in DB
    def test_unique_domain_id_with_factory(self):
        with self.assertRaises(Exception):
            FactoryForPfam(domain_id=self.pfam.domain_id)

class DomainModelWithFactoryPassingTest(TestCase):
    def setUp(self):
        # create object 
        self.domain = FactoryForDomain()

   # test field is not None
    def test_pfam_field_not_none_with_factory(self):
        self.assertIsNotNone(self.domain.pfam)

    # test creation of new object with indicated values 
    def test_create_new_domain_with_factory(self):
        domain = FactoryForDomain(
            domain_description='domain_description865_2',
            pfam=FactoryForPfam(domain_id='domain865_2', domain_description='description865_2')
        )
        # validated description = expected output
        self.assertEqual(domain.domain_description, 'domain_description865_2')


class DomainAssignmentModelWithFactoryPassingTest(TestCase):
    def setUp(self):
        # create object 
        self.domain_assignment = FactoryForDomainAssignment()
    
    # try to create another object with the same values
    def test_unique_together_with_factory(self):
        # validate exception is raised 
        with self.assertRaises(IntegrityError):
            FactoryForDomainAssignment(
                protein=self.domain_assignment.protein,
                domain=self.domain_assignment.domain,
                start=self.domain_assignment.start,
                end=self.domain_assignment.end
            )

################# END TESTS with Factory Boy

# ###########################################
# ## 3) FAILING TESTS

# class OrganismModelFailingTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         Organism.objects.create(taxa_id=1, clade='Clade865', genus='Genus865', species='Species865')

#     def test_create_organism_with_same_taxa_id_failing(self):
#         with self.assertRaises(Exception):
#             Organism.objects.create(taxa_id=1, clade='Clade865', genus='Genus865', species='test2')

# class ProteinModelFailingTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         # Set up non-modified objects used by all test methods
#         organism = Organism.objects.create(taxa_id=1, clade='Clade865', genus='Genus865', species='Species865')
#         Protein.objects.create(protein_id='protein865', sequence='sequence865', length=18, organism=organism)

#     def test_create_new_protein_with_same_protein_id_failing(self):
#         organism = Organism.objects.create(taxa_id=2, clade='Clade865', genus='Genus865', species='test2')
#         Protein.objects.create(protein_id='protein865', sequence='test_sequence_2', length=20, organism=organism)
#         with self.assertRaises(Exception):
#             Protein.objects.create(protein_id='protein865', sequence='test_sequence_2', length=20, organism=organism)

# class PfamModelFailingTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         Pfam.objects.create(domain_id='domain865', domain_description='description865')

#     def test_create_pfam_with_same_domain_id_failing(self):
#         with self.assertRaises(IntegrityError):
#             Pfam.objects.create(domain_id='domain865', domain_description='description865')

# class DomainModelFailingTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         pfam = Pfam.objects.create(domain_id='domain865', domain_description='description865')
#         Domain.objects.create(domain_description='domain_description865', pfam=pfam)

#     def test_create_domain_with_same_domain_description_failing(self):
#         with self.assertRaises(Exception):
#             pfam = Pfam.objects.create(domain_id='domain865_2', domain_description='description865_2')
#             Domain.objects.create(domain_description='domain_description865', pfam=pfam)

# class DomainAssignmentModelFailingTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         organism = Organism.objects.create(taxa_id=1, clade='Clade865', genus='Genus865', species='Species865')
#         protein = Protein.objects.create(protein_id='protein865', sequence='sequence865', length=18, organism=organism)
#         pfam = Pfam.objects.create(domain_id='domain865', domain_description='description865')
#         domain = Domain.objects.create(domain_description='domain_description865', pfam=pfam)
#         DomainAssignment.objects.create(protein=protein, domain=domain, start=1, end=19)

#     def test_create_domain_assignment_failing(self):
#         organism = Organism.objects.create(taxa_id=2, clade='Clade865', genus='Genus865', species='test2')
#         protein = Protein.objects.create(protein_id='protein865_2', sequence='test_sequence_2', length=20, organism=organism)
#         pfam = Pfam.objects.create(domain_id='domain865_2', domain_description='description865_2')
#         domain = Domain.objects.create(domain_description='domain_description865_2', pfam=pfam)
#         domain_assignment = DomainAssignment.objects.create(protein=protein, domain=domain, start=1, end=20)
#         self.assertEqual(str(domain_assignment), 'protein865_2, test_domain_description_2 (1-20)')

#     def test_create_domain_assignment_with_invalid_start_position_failing(self):
#         organism = Organism.objects.create(taxa_id=2, clade='Clade865', genus='Genus865', species='test2')
#         protein = Protein.objects.create(protein_id='protein865_2', sequence='test_sequence_2', length=20, organism=organism)
#         pfam = Pfam.objects.create(domain_id='domain865_2', domain_description='description865_2')
#         domain = Domain.objects.create(domain_description='domain_description865_2', pfam=pfam)
#         with self.assertRaises(Exception):
#             DomainAssignment.objects.create(protein=protein, domain=domain, start=21, end=30)

#     def test_create_domain_assignment_with_invalid_end_position_failing(self):
#         organism = Organism.objects.create(taxa_id=2, clade='Clade865', genus='Genus865', species='test2')
#         protein = Protein.objects.create(protein_id='protein865_2', sequence='test_sequence_2', length=20, organism=organism)
#         pfam = Pfam.objects.create(domain_id='domain865_2', domain_description='description865_2')
#         domain = Domain.objects.create(domain_description='domain_description865_2', pfam=pfam)
#         with self.assertRaises(Exception):
#             DomainAssignment.objects.create(protein=protein, domain=domain, start=10, end=25)

#     def test_create_domain_assignment_with_invalid_protein_object_failing(self):
#         pfam = Pfam.objects.create(domain_id='domain865_2', domain_description='description865_2')
#         domain = Domain.objects.create(domain_description='domain_description865_2', pfam=pfam)
#         with self.assertRaises(Exception):
#             DomainAssignment.objects.create(protein_id='invalid_protein', domain=domain, start=1, end=19)

# ########### END FAILING TESTS

# END: I wrote the code based on documentation and references. Important links were included in the comments. 
# Please review links below and short commentary in readme.txt. Thank you.
