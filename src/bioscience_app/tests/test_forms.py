from django.test import TestCase
from django.forms.models import model_to_dict
from ..forms import NewProteinForm
from bioscience_app.forms import NewProteinForm, FormForOrganism, FormForPfam, FormForDomain, FormForDomainAssignment


# START: I wrote the code based on documentation and references. 
# Please review short commentary in readme.txt. Thank you.


from bioscience_app.tests.factories import (
    FactoryForOrganism, 
    FactoryForProtein,
    FactoryForPfam,
    FactoryForDomain,
    FactoryForDomainAssignment
)

class NewProteinFormPassingTest(TestCase):
    # test if form has valid data
    def test_form_for_valid_data(self):
        organism = FactoryForOrganism.create()
        protein = FactoryForProtein.build(organism=organism)
        data = model_to_dict(protein, exclude=['id'])
        form = NewProteinForm(data)
        self.assertTrue(form.is_valid())

    # test if form doesnt have protein id
    def test_form_without_protein_id(self):
        organism = FactoryForOrganism.create()
        protein = FactoryForProtein.build(protein_id=None, organism=organism)
        data = model_to_dict(protein, exclude=['id'])
        form = NewProteinForm(data)
        self.assertFalse(form.is_valid())

    # test if error message present protein id is missing
    def test_error_message_if_protein_id_is_missing(self):
        organism = FactoryForOrganism.create()
        protein = FactoryForProtein.build(protein_id=None, organism=organism)
        data = model_to_dict(protein, exclude=['id'])
        form = NewProteinForm(data)
        self.assertEqual(form.errors['protein_id'], ['This field is required.'])


class FormForOrganismTest(TestCase):
    # test if form has valid data
    def test_form_for_valid_data(self):
        data = FactoryForOrganism.build().__dict__
        form = FormForOrganism(data)
        self.assertTrue(form.is_valid())

    # test if form doesnt have taxa id
    def test_form_without_taxa_id(self):
        data = FactoryForOrganism.build(taxa_id=None).__dict__
        form = FormForOrganism(data)
        self.assertFalse(form.is_valid())

   # test if error message present taxa id is missing 
    def test_error_message_if_taxa_id_is_missing(self):
        data = FactoryForOrganism.build(taxa_id=None).__dict__
        form = FormForOrganism(data)
        self.assertEqual(form.errors['taxa_id'], ['This field is required.'])

class FormForPfamTest(TestCase):
    # test if form has valid data
    def test_form_for_valid_data(self):
        pfam = FactoryForPfam.build()  
        data = model_to_dict(pfam)  
        form = FormForPfam(data) 
        self.assertTrue(form.is_valid()) 

    # test if form doesnt have domain id
    def test_form_witout_domain_id(self):
        pfam = FactoryForPfam.build(domain_id=None)  
        data = model_to_dict(pfam)
        form = FormForPfam(data)
        self.assertFalse(form.is_valid())  
 
    # test if error message present if domain id is missing 
    def test_error_message_if_domain_id_is_missing(self):
        pfam = FactoryForPfam.build(domain_id=None)
        data = model_to_dict(pfam)
        form = FormForPfam(data)
        self.assertEqual(form.errors['domain_id'], ['This field is required.'])  

class FormForDomainTest(TestCase):
      # test if form has valid data
    def test_form_for_valid_data(self):
        pfam = FactoryForPfam.create()  
        domain = FactoryForDomain.build(pfam=pfam)  
        data = model_to_dict(domain)  
        form = FormForDomain(data)  
        self.assertTrue(form.is_valid())  

    # test if form doesnt have domain description
    def test_form_without_domain_description(self):
        domain = FactoryForDomain.build(domain_description=None) 
        data = model_to_dict(domain)
        form = FormForDomain(data)
        self.assertFalse(form.is_valid()) 

    # test if error message present if domain description is missing 
    def test_error_message_if_domain_description_is_missing(self):
        domain = FactoryForDomain.build(domain_description=None)
        data = model_to_dict(domain)
        form = FormForDomain(data)
        self.assertEqual(form.errors['domain_description'], ['This field is required.']) 

class FormForDomainAssignmentTest(TestCase):
    # test if form has valid data
    def test_form_for_valid_data(self):
        protein = FactoryForProtein.create()  
        domain = FactoryForDomain.create()  
        domain_assignment = FactoryForDomainAssignment.build(protein=protein, domain=domain)  
        data = model_to_dict(domain_assignment)
        form = FormForDomainAssignment(data)
        self.assertTrue(form.is_valid())

    # test if start is not positive(negative)
    def test_form_if_start_is_negative(self):
        domain_assignment = FactoryForDomainAssignment.build(start=-1)
        data = model_to_dict(domain_assignment)
        form = FormForDomainAssignment(data)
        self.assertFalse(form.is_valid())

    # tests if form doesnt have protein id
    def test_form_without_protein(self):
        domain_assignment = FactoryForDomainAssignment.build(protein=None)
        data = model_to_dict(domain_assignment)
        form = FormForDomainAssignment(data)
        self.assertFalse(form.is_valid())

    # test if error message is present  
    def test_form_for_error_message_no_protein(self):
        domain_assignment = FactoryForDomainAssignment.build(protein=None)
        data = model_to_dict(domain_assignment)
        form = FormForDomainAssignment(data)
        self.assertEqual(form.errors['protein'], ['This field is required.'])

    # test if form doesnt have domain
    def test_form_without_domain(self):
        domain_assignment = FactoryForDomainAssignment.build(domain=None)
        data = model_to_dict(domain_assignment)
        form = FormForDomainAssignment(data)
        self.assertFalse(form.is_valid())

    # tests if error message is prensent
    def test_form_for_error_message_if_no_domain(self):
        domain_assignment = FactoryForDomainAssignment.build(domain=None)
        data = model_to_dict(domain_assignment)
        form = FormForDomainAssignment(data)
        self.assertEqual(form.errors['domain'], ['This field is required.'])


# END: I wrote the code based on documentation and references. 
# Please review short commentary in readme.txt. Thank you.






