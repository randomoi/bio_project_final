from django.shortcuts import get_object_or_404, render
from rest_framework import generics
from rest_framework.response import Response
from .models import Protein, Organism, Domain,  Pfam  
from .serializers import SerializerForProtein, DomainAssignment, SerializerForPfam, SerializerForProteinByTaxa, SerializerForDomainByTaxa
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination


# START: I wrote the code based on documentation and references. Important links were included in the comments next to each function. 
# Please review links below and short commentary in readme.txt. Thank you.

# https://www.django-rest-framework.org/api-guide/generic-views/#genericapiview
# https://www.django-rest-framework.org/api-guide/generic-views/#listapiview
# handles view for Protein by Taxa
class ListProteinByTaxaView(generics.ListAPIView):
    serializer_class = SerializerForProteinByTaxa

    def get_queryset(self):
        taxa_id = self.kwargs['taxa_id'] # get taxa_id from the URL
        organisms = Organism.objects.filter(taxa_id=taxa_id) # get organisms with indicated taxa_id
        return Protein.objects.filter(organism__in=organisms) # get proteins from organism 

# https://www.django-rest-framework.org/api-guide/generic-views/#genericapiview
# https://www.django-rest-framework.org/api-guide/generic-views/#listapiview
# handles view for Domain by Taxa
class ListDomainByTaxaView(generics.ListAPIView):
    serializer_class = SerializerForDomainByTaxa

    def get_queryset(self):
        taxa_id = self.kwargs['taxa_id'] # get taxa_id from the URL
        domain_assignments = DomainAssignment.objects.filter(protein__organism__taxa_id=taxa_id) # get domain assignments from proteins with indicated taxa_id
        domain_ids = domain_assignments.values_list('domain_id', flat=True) # get domain ids from domain assignments
        return Domain.objects.filter(id__in=domain_ids) 

# https://www.django-rest-framework.org/api-guide/views/#api-reference
# https://docs.djangoproject.com/en/3.2/ref/models/instances/#django.db.models.Model.DoesNotExist
# https://www.django-rest-framework.org/api-guide/responses/#response
# https://docs.python.org/3/library/functions.html#sum
# https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions
# https://docs.python.org/3/reference/expressions.html#binary-arithmetic-operations
# handles view for Coverage
class CoverageView(APIView):
    def get(self, request, protein_id):
        try:
            protein = Protein.objects.get(protein_id=protein_id) # get protein with indicated protein_id
        except Protein.DoesNotExist:
            return Response({'error': 'Protein was not found.'}, status=404) # if the protein does not exist, return an error response

        domain_assignments = DomainAssignment.objects.filter(protein=protein) # get domain assignments for protein
        sum_of_domain_length = sum([assignment.end - assignment.start + 1 for assignment in domain_assignments]) # calculate the total length of all domains assigned to the protein
        coverage = sum_of_domain_length / protein.length # calculate coverage (ratio of total domain length/protein length)
        return Response({'coverage': coverage}) # return response

# sets limit on how many records are displayed for http://127.0.0.1:8000/api/protein/
# references: https://www.django-rest-framework.org/api-guide/pagination/
# https://www.django-rest-framework.org/api-guide/pagination/#limitoffsetpagination
# https://docs.djangoproject.com/en/4.1/ref/models/querysets/
# https://www.django-rest-framework.org/api-guide/views/
# https://www.django-rest-framework.org/api-guide/generic-views/
# handles limiting records on Protein page, this helps it load faster. There is is list of page on the page so all records can be viewed (there are a lot of them)
class LimitRecords(LimitOffsetPagination):
    default_limit = 1 # use default variable to set 1 record as limit 

# https://www.django-rest-framework.org/api-guide/generic-views/#listcreateapiview
# https://www.django-rest-framework.org/api-guide/generic-views/#retrieveupdatedestroyapiview
# https://www.django-rest-framework.org/api-guide/generic-views/#retrieveapiview
# https://docs.djangoproject.com/en/3.2/ref/models/querysets/#django.db.models.query.QuerySet.all
# https://docs.djangoproject.com/en/3.2/ref/models/querysets/#django.db.models.query.QuerySet.all
# https://www.django-rest-framework.org/api-guide/generic-views/#lookup-field
# https://www.django-rest-framework.org/api-guide/serializers/#specifying-which-fields-to-include
# handles view for create new protein 
class CreateNewProteinView(generics.ListCreateAPIView):
    queryset = Protein.objects.all() # get all proteins from DB
    serializer_class = SerializerForProtein # uses SerializerForProtein for serialization 
    pagination_class = LimitRecords # uses custom pagination defined in LimitRecords class

# handles view for Protein by ID
class RetrieveProteinByIDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Protein.objects.all() # get proteins from DB
    serializer_class = SerializerForProtein # uses SerializerForProtein for serialization 
    lookup_field = 'protein_id' # uses protein id field for getting a specified protein 
    fields = ['protein_id', 'sequence', 'taxonomy', 'length', 'domains', 'organism'] # fields to be displayed

# handles view for Pfam details
class RetrievePfamDetailsView(generics.RetrieveAPIView):
    queryset = Pfam.objects.all() # get Pfam domains from DB
    serializer_class = SerializerForPfam # uses SerializerForPfam for serialization
    lookup_field = 'domain_id' # uses domain_id for getting an indicated Pfam domain


# END: I wrote the code based on documentation and references. Important links were included in the comments next to each function. 
# Please review links below and short commentary in readme.txt. Thank you.