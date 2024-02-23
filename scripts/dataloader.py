import pandas as pd

class DataArranger:
    def __init__(self, file_path_to_xlsx, names=True):
        # Initialize the DataArranger class with the path to the Excel file
        self.file_path_to_xlsx = file_path_to_xlsx
        self.hydron_dataset = pd.read_excel(file_path_to_xlsx)  # Read the Excel file into a pandas DataFrame
        
        # Set the ground_truth attribute based on the specified column name
        if names:
            self.ground_truth = self.hydron_dataset["NER Ground Truth Names"]
        else:
            self.ground_truth = self.hydron_dataset["NER Ground Truth Measures"]
        self.names = names

    def return_ground_truth(self):
        def extract_first_word(cell_value):
            # Helper function to extract the first word from each line in the cell
            lines = str(cell_value).split(';')
            if self.names:
                first_words = [line.split(',')[0].strip() for line in lines if line]
            else:
                first_words = [line.split(',')[-1].strip() for line in lines if line]
            return ', '.join(first_words)

        # Apply the helper function to extract first words and return them as a list
        return self.ground_truth.apply(extract_first_word)

    def replace_abbreviations(self, col_name):
        # Dictionary of abbreviations and their corresponding full forms
        acronym_dict = [('spo2', 'supplemental oxygen'),
                        ('resp', 'respiratory rate'),
                        ('bp', 'blood pressure'),
                        ('gcs', 'glasgow coma score'),
                        ('ekg', 'electrocardiogram'),
                        ]

        def replace_acronyms(text):
            # Helper function to replace abbreviations in the text
            for acronym, full_form in acronym_dict:
                text = text.replace(acronym, full_form)
            return text

        # Apply the helper function to replace acronyms in the specified column
        self.hydron_dataset[col_name] = self.hydron_dataset[col_name].apply(replace_acronyms)
        self.hydron_dataset.to_excel(self.file_path_to_xlsx)

    def return_sentences(self):
        # Return the first 12 sentences from the 'Transcription' column
        return self.hydron_dataset['Transcription']

    def add_ground_truth_column(self, column_name):
        # Add a new column with extracted ground truth information and replace abbreviations
        self.hydron_dataset[column_name] = self.return_ground_truth()
        self.replace_abbreviations(col_name=column_name)

    def add_column(self, df, col_name):
        # Add a new column to the dataset and save the updated dataset to the Excel file
        self.hydron_dataset[col_name] = df[col_name]
        self.hydron_dataset.to_excel(self.file_path_to_xlsx)
