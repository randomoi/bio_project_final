from django.db import models

# START: I wrote the code based on documentation and references. Important links were included in the comments next to each function. 
# Please review links below and short commentary in readme.txt. Thank you.

# https://docs.djangoproject.com/en/3.2/ref/models/fields/
# https://docs.djangoproject.com/en/3.2/ref/models/options/
# https://docs.djangoproject.com/en/3.2/topics/db/models/#relationships
# https://docs.djangoproject.com/en/3.2/ref/models/instances/#str

# create Organism model which uses Django Model 
class Organism(models.Model):
    # create field taxa_id with optional null value
    taxa_id = models.IntegerField(null=True)
    # create field clade with max length of 100 char
    clade = models.CharField(max_length=100)
     # create field genus with max length of 100 char (genus species name is split during data loading)
    genus = models.CharField(max_length=100)
    # create field species with max length of 100 char (genus species name is split during data loading)
    species = models.CharField(max_length=100)

    # create method that returns a string 
    def __str__(self):
        # returns formatted string 
        return f"{self.taxa_id}, {self.clade}, {self.genus}, {self.species}"

    # create unique combination 
    class Meta:
        unique_together = ('taxa_id', 'clade', 'genus', 'species')


# create Protein model which uses Django Model 
class Protein(models.Model):
    # create a primary key field protein_id with max length 50 char
    protein_id = models.CharField(max_length=50, primary_key=True)
    # create text field sequence 
    sequence = models.TextField()
    # create field length with default value 0
    length = models.IntegerField(default=0)
    # create a foreign key field organism (Organism model)
    # when Organism is deleted then all Protein objects belonging to it deleted too
    # related_name allows querying related Proteins from Organism 
    organism = models.ForeignKey(Organism, on_delete=models.CASCADE, related_name='proteins')
    # create field id_custom which allows null and blank values
    id_custom = models.IntegerField(null=True, blank=True)

    # create method that returns a string 
    def __str__(self):
            # returns formatted string 
            return f"{self.protein_id} (Organism: {self.organism.genus} {self.organism.species})"


# create Pfam model which uses Django Model 
class Pfam(models.Model):
    # create a primary key field domain_id with max length 50 char
    domain_id = models.CharField(max_length=50, primary_key=True)
    # create field domain_description with max length 200 char
    domain_description = models.CharField(max_length=200)

    # create method that returns a string 
    def __str__(self):
        # returns formatted string 
        return f"{self.domain_id}: {self.domain_description}"


# create Domain model which uses Django Model 
class Domain(models.Model):
    # create field domain_description with max length 200 char
    domain_description = models.CharField(max_length=200)
    # create a foreign key field pfam (Pfam model) 
    #  when a Pfam is deleted then all Domain objects belonging to it deleted too
    #  allows null and blank values 
    pfam = models.ForeignKey(Pfam, on_delete=models.CASCADE, null=True, blank=True)


# create Domain Assignment model which uses Django Model 
class DomainAssignment(models.Model):
    # create a foreign key field protein which uses Protein model. 
    # when a Protein object is deleted, all DomainAssignment objects belonging to it deleted too 
    # related_name allows querying related Domain Assignments from Protein object
    protein = models.ForeignKey(Protein, on_delete=models.CASCADE, related_name='domain_assignments')
    # create foreign key field domain which uses Domain model
    # when Domain object is deleted, all Domain Assignment objects belonging to it deleted too
    # related_name allows querying related Domain Assignments from Domain object
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, related_name='domain_assignments')
    # create field start 
    start = models.IntegerField()
    # create field end 
    end = models.IntegerField()

    # create unique combination 
    class Meta:
        unique_together = ('protein', 'domain', 'start', 'end')

     # create method that returns a string 
    def __str__(self):
        # returns formatted string 
        return f"{self.protein.protein_id} ({self.protein.organism.genus} {self.protein.organism.species}) - {self.domain.domain_description} - {self.start}-{self.end}"


# END: I wrote the code based on documentation and references. Important links were included in the comments next to each function. 
# Please review links below and short commentary in readme.txt. Thank you.
