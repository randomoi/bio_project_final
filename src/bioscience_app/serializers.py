from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import Protein, Organism, Domain, Pfam, DomainAssignment

# START: I wrote the code based on documentation and references. Important links were included in the comments next to each function. 
# Please review links below and short commentary in readme.txt. Thank you.

# https://www.django-rest-framework.org/api-guide/serializers/
# https://docs.djangoproject.com/en/3.2/topics/http/shortcuts/#get-object-or-404
# https://www.django-rest-framework.org/api-guide/serializers/#modelserializer
# https://www.django-rest-framework.org/api-guide/fields/#serializermethodfield
# https://www.django-rest-framework.org/api-guide/serializers/#serializer-class
# https://docs.djangoproject.com/en/3.2/topics/serialization/
# https://docs.djangoproject.com/en/3.2/topics/serialization/#module-django.core.serializers
# https://www.django-rest-framework.org/api-guide/relations/#nested-relationships
# https://www.django-rest-framework.org/api-guide/serializers/#saving-instances
# https://www.django-rest-framework.org/api-guide/fields/#source
# https://docs.djangoproject.com/en/3.2/ref/models/querysets/#get-or-create

# serializer Organism uses ModelSerializer
class SerializerForOrganism(serializers.ModelSerializer):
    # specifies the model and fields for inclusion 
    class Meta:
        model = Organism
        fields = '__all__'


# serializer Pfam uses ModelSerializer
class SerializerForPfam(serializers.ModelSerializer):
    # specifies the model and fields for inclusion 
    class Meta:
        model = Pfam
        fields = ['domain_id', 'domain_description']

# serializer for Domain by Taxa uses ModelSerializer 
class SerializerForDomainByTaxa(serializers.ModelSerializer):
    # create field pfam_id and assign it to value from the pfam object which is serialized by SerializerForPfam 
    pfam_id = SerializerForPfam(source='pfam')

    # specifies the model and fields for inclusion 
    class Meta:
        model = Domain
        fields = ['id', 'pfam_id']


# serializer for Domain Assignment uses ModelSerializer 
class SerializerForDomainAssignment(serializers.ModelSerializer):
    # create field pfam_id it will be computed by get_pfam_id method (see below) 
    pfam_id = SerializerForPfam(source='domain.pfam')
    # create field description which gets value from pfam.domain_description field  
    description = serializers.CharField(source='domain.pfam.domain_description')
    # create field start which gets value from domain_assignment's start field
    start = serializers.IntegerField()
    # create field stop which gets value from the domain's end field
    stop = serializers.IntegerField(source='end')

    # specifies the model and fields for inclusion 
    class Meta:
        model = DomainAssignment
        fields = ['pfam_id', 'description', 'start', 'stop']


# serializer for SerializerForProteinByTaxa use ModelSerializer 
class SerializerForProteinByTaxa(serializers.ModelSerializer):
    # create field id which gets value from id_custom 
    id = serializers.IntegerField(source='id_custom')
    # create field protein_id which gets value from protein_id 
    protein_id = serializers.CharField()

    # specifies the model and fields for inclusion 
    class Meta:
        model = Protein
        fields = ('id', 'protein_id')


# serializer for SerializerForProtein using ModelSerializer 
class SerializerForProtein(serializers.ModelSerializer):
    # create field taxonomy which uses OrganismSerializer
    taxonomy = SerializerForOrganism(source='organism')
    # create field domains (has many-to-many relationship)
    domains = SerializerForDomainAssignment(many=True, source='domain_assignments')

    class Meta:
        model = Protein # model used
        fields = ['protein_id', 'sequence', 'taxonomy', 'length', 'domains'] # fields used

    # override method 
    def create(self, validated_data):
        # "pop" data from validated data
        domain_assignments_data = validated_data.pop('domain_assignments')
        organism_data = validated_data.pop('organism')

         # instances creation
        organism = Organism.objects.create(**organism_data)
        protein = Protein.objects.create(organism=organism, **validated_data)


    # create domain + domain assignment instance for every domain assignment
        for domain_assignment_data in domain_assignments_data:
            domain_data = domain_assignment_data.pop('domain')
            pfam_data = domain_data.pop('pfam')
            pfam, _ = Pfam.objects.get_or_create(**pfam_data)
            domain, _ = Domain.objects.get_or_create(pfam=pfam, **domain_data)
            DomainAssignment.objects.create(protein=protein, domain=domain, **domain_assignment_data)
   
        return protein

     # override method  
    def update(self, instance, validated_data):
        # "pop" data from validated data
        domain_assignments_data = validated_data.pop('domain_assignments')
        organism_data = validated_data.pop('organism')
        # organism instance by using get or create 
        organism, created = Organism.objects.get_or_create(**organism_data)
        # if not created update fields (meaning it exists)
        if not created:
            for attr, value in organism_data.items():
                setattr(organism, attr, value)
            organism.save()

        instance.organism = organism
        # update protein instance with super class
        instance = super().update(instance, validated_data)


         # domain assignment instance by using get or create, for every domain assignment
        for domain_assignment_data in domain_assignments_data:
            domain_assignment, created = DomainAssignment.objects.get_or_create(protein=instance, **domain_assignment_data)
            if not created:
                # if not created update fields (meaning it exists)
                for attr, value in domain_assignment_data.items():
                    setattr(domain_assignment, attr, value)
                domain_assignment.save()

        return instance


# END: I wrote the code based on documentation and references. Important links were included in the comments next to each function. 
# Please review links below and short commentary in readme.txt. Thank you.