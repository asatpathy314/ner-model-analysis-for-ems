import os
from time import sleep
from pymetamap import MetaMap
from dataloader import DataArranger
import pandas as pd
import re

class MetaMapEntityExtractor:
    def __init__(self, base_dir, bin_dir='/bin/metamap16', pos_server_dir='/bin/skrmedpostctl', wsd_server_dir='/bin/wsdserverctl'):
        # Initialize MetaMapEntityExtractor with the provided directory paths
        self.metamap_base_dir = base_dir
        self.metamap_bin_dir = bin_dir
        self.metamap_pos_server_dir = pos_server_dir
        self.metamap_wsd_server_dir = wsd_server_dir

    def start_servers(self):
        # Start the MetaMap part-of-speech tagger server
        os.system(self.metamap_base_dir + self.metamap_pos_server_dir + ' start')
        # Start the MetaMap word sense disambiguation server
        os.system(os.path.join(self.metamap_base_dir + self.metamap_wsd_server_dir + ' start'))
        # Sleep to allow time for the servers to start (adjust if needed)
        sleep(60)

    def extract_concepts_to_file(self, note_list, file_path="metamap_concepts.txt", tag_restrictions=None, preferred_name = True):
        # Create a MetaMap instance
        mm = MetaMap.get_instance(os.path.join(self.metamap_base_dir + self.metamap_bin_dir))

        # List to store lists of concepts for each note
        list_of_list_of_concepts = []

        # Extract concepts for each note in the provided list
        for note in note_list:
            if tag_restrictions:
                cons, errs = mm.extract_concepts([note], word_sense_disambiguation=True, restrict_to_sts=tag_restrictions)
            else:
                cons, errs = mm.extract_concepts([note], word_sense_disambiguation=True)

            # Extract preferred names of concepts and store in a list
            if preferred_name:
                list_of_concepts = [con.preferred_name for con in cons]
            else:
                for con in cons:
                    list_of_concepts = []
                    try:
                        string = con.trigger
                        string = string[string.find('tx')+6:]
                        string = string[:string.find('"')]
                    except IndexError:
                        pass

        # Write the list of lists of concepts to a file
        with open(file_path, "w") as f:
            f.write(str(list_of_list_of_concepts))


    def extract_concepts_as_df(self, note_list, col_name, tag_restrictions=None, preferred_name=True):
        # Create a MetaMap instance
        mm = MetaMap.get_instance(os.path.join(self.metamap_base_dir + self.metamap_bin_dir))

        # Create an empty DataFrame to store the concepts
        df = pd.DataFrame(columns=[col_name])

        # Extract concepts for each note in the provided list
        for note in note_list:
            if tag_restrictions:
                cons, errs = mm.extract_concepts([note], word_sense_disambiguation=True, restrict_to_sts=tag_restrictions)
            else:
                cons, errs = mm.extract_concepts([note], word_sense_disambiguation=True)

            # Extract preferred names of concepts and store in a list
            '["Passenger"-tx-1-"passenger"-noun-0]'
            if preferred_name:
                list_of_concepts = [con.preferred_name for con in cons]
            else:
                list_of_concepts = []
                for con in cons:
                    string = con.trigger
                    string = string[string.find('tx')+6:]
                    string = string[:string.find('"')]  
                    list_of_concepts.append(string)
            # Append the concepts for the current note to the DataFrame
            df.loc[len(df.index)] = ', '.join(list_of_concepts)

        return df  # Return the entire DataFrame, not just a column


    """
    # Tags relevant for EMS NLP
    tags_for_ems_nlp = [
        'acab',  # Acquired Abnormality
        'aggp',  # Age Group
        'anab',  # Anatomical Abnormality
        'anim',  # Animal
        'bact',  # Bacterium
        'bdsy',  # Body System
        'bpoc',  # Body Part, Organ, or Organ Component
        'clnd',  # Clinical Drug
        'diap',  # Diagnostic Procedure
        'dsyn',  # Disease or Syndrome
        'fndg',  # Finding
        'inpo',  # Injury or Poisoning
        'medd',  # Medical Device
        'mobd',  # Mental or Behavioral Dysfunction
        'phsu',  # Pharmacologic Substance
        'phob',  # Physical Object
        'sosy',  # Sign or Symptom
        'tmco',  # Temporal Concept
        'topp'   # Therapeutic or Preventive Procedure
    ]
    """