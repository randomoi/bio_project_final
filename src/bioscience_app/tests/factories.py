import factory
from bioscience_app.models import Organism, Protein, Pfam, Domain, DomainAssignment
from factory.fuzzy import FuzzyInteger
from faker import Faker
from random import randint


# START: I wrote the code based on documentation and references. Important links were included in the comments next to each function. 
# Please review links below and short commentary in readme.txt. Thank you.

# https://factoryboy.readthedocs.io/
# https://github.com/FactoryBoy/factory_boy
# https://faker.readthedocs.io/
# https://github.com/joke2k/faker

fake = Faker()

# create factory for Organism
class FactoryForOrganism(factory.django.DjangoModelFactory):
    class Meta:
        model = Organism

    taxa_id = FuzzyInteger(1, 10000)
    clade = factory.Faker('word')
    genus = factory.Faker('word')
    species = factory.Faker('word')

# create factory for Protein 
class FactoryForProtein(factory.django.DjangoModelFactory):
    class Meta:
        model = Protein

    protein_id = factory.Sequence(lambda n: f'protein{n}')
    sequence = factory.Faker('text', max_nb_chars=40000)  # max sequence length
    length = factory.LazyAttribute(lambda obj: len(obj.sequence))  # length = sequence
    organism = factory.SubFactory(FactoryForOrganism)
    id_custom = factory.Faker('random_int')

# create factory for Pfam 
class FactoryForPfam(factory.django.DjangoModelFactory):
    class Meta:
        model = Pfam

    domain_id = factory.Sequence(lambda n: f'domain{n}')
    domain_description = factory.Faker('sentence', nb_words=6, variable_nb_words=True)  

# create factory for Domain
class FactoryForDomain(factory.django.DjangoModelFactory):
    class Meta:
        model = Domain

    domain_description = factory.Faker('sentence', nb_words=6, variable_nb_words=True)  
    pfam = factory.SubFactory(FactoryForPfam)

# create factory for DomainAssignment
class FactoryForDomainAssignment(factory.django.DjangoModelFactory):
    class Meta:
        model = DomainAssignment

    protein = factory.SubFactory(FactoryForProtein)
    domain = factory.SubFactory(FactoryForDomain)
    start = FuzzyInteger(1, 25000)
    end = factory.LazyAttribute(lambda o: o.start + randint(1, 25000))  # start first then end 


# END: I wrote the code based on documentation and references. Important links were included in the comments next to each function. 
# Please review links below and short commentary in readme.txt. Thank you.
