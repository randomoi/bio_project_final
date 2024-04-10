import sys # allows to work with Python Sys 
import os # allows to work with OS 
import csv # allows to work with CSV documents
from django.core.wsgi import get_wsgi_application 

import django # allows to work with Django

# START: I wrote the code based on documentation and references. Important links were included in the comments next to each function. 
# Please review links below and short commentary in readme.txt. Thank you.

# https://docs.python.org/3/library/sys.html#sys.path
# https://docs.python.org/3/library/os.path.html
# https://docs.python.org/3/library/os.html#os.environ
# https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/#django.core.wsgi.get_wsgi_application

sys.path.append(os.path.dirname(os.path.abspath(__file__))) # add the directory of file to system path
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..") # add the directory of parent file directory to system path
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bioscience.settings") # set the default environment 

django.setup()

from bioscience_app.models import Protein, Domain, Organism, DomainAssignment, Pfam # django models 

application = get_wsgi_application() # assigning the WSGI to application 

# https://docs.python.org/3/library/functions.html#open
# https://docs.python.org/3/library/csv.html#csv.reader
# https://docs.python.org/3/library/os.path.html
# https://docs.djangoproject.com/en/3.2/ref/models/querysets/#get-or-create
# https://docs.djangoproject.com/en/3.2/ref/models/instances/#django.db.models.Model.save
# https://docs.python.org/3/library/exceptions.html

def load_assignment_data_sequences(file_path):
    try:
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data_files', file_path), 'r') as f: # open the "assignment_data_sequences.csv"
            csv_reader = csv.reader(f) # assign variable to create CSV reader
            for row in csv_reader: # go through each row 
                protein_id, sequence = row # assign variables into rows 
                organism, _ = Organism.objects.get_or_create(genus="Unspecified", species="Unspecified", defaults={"taxa_id": -1}) # specifying default values for organism 
                protein, _ = Protein.objects.get_or_create(protein_id=protein_id, defaults={"organism": organism}) # specifying default values for protein 
                protein.sequence = sequence # setting sequence 
                protein.save() # saving to DB
    
    # error checking
    except FileNotFoundError: # if file is not found print an error
        print(f"Error: The '{file_path}' is not found.")
    
    except IOError: # if file can not be read print an error
        print(f"Error: Can not read '{file_path}'.")
    
    except Exception as e: # if there is some other error, print the error message
        print(f"Error: Unexpected error! Check your code and file. {e}")


# https://docs.python.org/3/library/os.path.html
# https://docs.python.org/3/library/csv.html
# https://docs.python.org/3/library/functions.html#open
# https://docs.python.org/3/library/os.path.html#os.path.abspath
# https://docs.python.org/3/library/os.path.html#os.path.dirname
# https://docs.python.org/3/library/os.path.html#os.path.join
# https://docs.djangoproject.com/en/3.2/topics/db/models/
# https://docs.python.org/3/library/exceptions.html

def load_assignment_data_set(file_path):
    try:
        id_custom = 80000  # custom id to start at 80000 
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data_files', file_path), 'r') as f: # open the "assignment_data_set.csv"
            csv_reader = csv.reader(f) # assign variable to create CSV reader
            for row in csv_reader: # go through each row 
                protein_id = row[0] # from 1st column get protein_id 
                taxa_id = int(row[1]) # from 2nd column get taxa_id 
                clade = row[2] # from 3rd column get clade 
                genus, species = row[3].split(" ")[:2] # from 4th column get genus and species names and separate them  
                domain_description = row[4] # from 5th column get description 
                domain_id_pfam = row[5] # from 6th column get pfam's domain_id 
                start = int(row[6]) # from 7th column get start 
                end = int(row[7]) # from 8th column get end
                length_protein = int(row[8]) # from 9th column get length

                organism, _ = Organism.objects.get_or_create( # organism instance with specified assigments 
                    taxa_id=taxa_id,
                    clade=clade,
                    genus=genus,
                    species=species,
                )

                protein, created = Protein.objects.get_or_create( # protein instance with specified assigments 
                    protein_id=protein_id,
                    defaults={
                        "organism": organism,
                        "length": length_protein,
                    }
                )

                protein.length = length_protein # assigning to received length 
                protein.organism = organism # assigning to received instance
                id_custom += 1  # incrementing by 1 
                protein.id_custom = id_custom  # assigning to custom id
                protein.save() # saving to DB

                instance_of_pfam, _ = Pfam.objects.get_or_create( # pfam instance with specified assigments 
                    domain_id=domain_id_pfam,
                    defaults={'domain_description': domain_description},
                )

                domain = Domain.objects.filter(pfam=instance_of_pfam).first() # get domain instance with Pfam instance

                if not domain: # if doesnt exist, create with specified assigments 
                    domain = Domain.objects.create(
                        pfam=instance_of_pfam,
                        domain_description=domain_description,
                    )

                exists = DomainAssignment.objects.filter( # validate if exists 
                    protein=protein,
                    domain=domain,
                    start=start,
                    end=end
                ).exists()

                if not exists: # if doesnt exist, create with specified assigments 
                    DomainAssignment.objects.create(
                        protein=protein,
                        domain=domain,
                        start=start,
                        end=end
                    )
    
    # error checking
    except FileNotFoundError: # if file is not found print an error
        print(f"Error: The '{file_path}' is not found.")
    
    except IOError: # if file can not be read print an error
        print(f"Error: Can not read '{file_path}'.")
    
    except Exception as e: # if there is some other error, print the error message
        print(f"Error: Unexpected error! Check your code and file. {e}")

# https://docs.python.org/3/library/os.path.html
# https://docs.python.org/3/library/csv.html
# https://docs.python.org/3/library/functions.html#open
# https://docs.python.org/3/library/os.path.html#os.path.abspath
# https://docs.python.org/3/library/os.path.html#os.path.dirname
# https://docs.python.org/3/library/os.path.html#os.path.join
# https://docs.djangoproject.com/en/3.2/topics/db/models/
# https://docs.python.org/3/library/exceptions.html

def load_data_pfam_descriptions(file_path):
    try:
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data_files', file_path), 'r') as csvfile: # open the "pfam_descriptions.csv"
            csv_reader = csv.reader(csvfile) # assign variable to create CSV reader
            for row in csv_reader: # go through each row 
                domain_id_pfam, description = row # assign variables into rows 
                domains = Domain.objects.filter(pfam__domain_id=domain_id_pfam)  # filter by domain_id_pfam 
               
                for domain in domains: # go through each domain
                    domain.domain_description = description  # assigning to received description
                    domain.save() # save to DB
    
    # error checking
    except FileNotFoundError: # if file is not found print an error
        print(f"Error: The '{file_path}' is not found.")
    
    except IOError: # if file can not be read print an error
        print(f"Error: Can not read '{file_path}'.")
    
    except Exception as e: # if there is some other error, print the error message
        print(f"Error: Unexpected error! Check your code and file. {e}")

# https://docs.djangoproject.com/en/3.2/topics/db/models/
# https://docs.djangoproject.com/en/3.2/topics/db/queries/#retrieving-objects
# https://docs.python.org/3/library/stdtypes.html#set
# https://docs.djangoproject.com/en/3.2/topics/db/queries/#deleting-objects
# https://docs.python.org/3/library/exceptions.html

def delete_duplicates():
    try:
        organisms = Organism.objects.all() # getting organisms
        distinct_organisms = set() # setting distinct set
        for organism in organisms: # go through all organisms
            distinct_id = (organism.taxa_id, organism.clade, organism.genus, organism.species) # id for distinct organisms
            if distinct_id in distinct_organisms: # if id matches distinct organism
                organism.delete() # delete it
            else:
                distinct_organisms.add(distinct_id) # otherwise add it to the set
    
    except TypeError as e:
        raise ValueError("Unable to delete duplicates.") from e

def main():
    assignment_data_sequences = 'assignment_data_sequences.csv' # assigning variable to the file
    assignment_data_set = 'assignment_data_set.csv' # assigning variable to the file
    pfam_descriptions = 'pfam_descriptions.csv' # assigning variable to the file
    
    load_assignment_data_sequences(assignment_data_sequences) # load specified file
    load_assignment_data_set(assignment_data_set) # load specified file
    load_data_pfam_descriptions(pfam_descriptions) # load specified file

if __name__ == '__main__':
    delete_duplicates() # delete duplicates from DB
    main() # add data to DB

# END: I wrote the code based on documentation and references. Important links were included in the comments next to each function. 
# Please review links below and short commentary in readme.txt. Thank you.