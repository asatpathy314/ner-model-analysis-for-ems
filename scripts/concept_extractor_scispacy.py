import spacy
from spacy import displacy
from dataloader import DataArranger
import pandas as pd

class SciSpacyEntityExtractor:
    def __init__(self, model_name):
        # Initialize the SciSpacyEntityExtractor with a specified SpaCy model and a data_arranger instance
        self.nlp = spacy.load(model_name)  # Load the specified SpaCy model
        self.data = DataArranger()  # Create an instance of the data_arranger class
        self.model_name = model_name

    def analyze_and_save_entities_to_html(self, output_file="entity.html"):
        # Get the data to be analyzed from the data_arranger instance
        data_to_be_analyzed = self.data.return_sentences()

        def display_entities(text):
            # Process the text with the SpaCy model to extract entities and create a displacy image
            doc = self.nlp(text)
            displacy_image = displacy.render(doc, jupyter=False, style='ent')
            # Extract entity information (text, label, start_char, end_char) for each entity in the document
            entity_and_label = [(ent.text, ent.label_, ent.start_char, ent.end_char) for ent in doc.ents]
            return displacy_image, entity_and_label

        # Analyze entities in the data and save the results to an HTML file
        with open(output_file, "w") as file:
            for text in data_to_be_analyzed:
                # Get displacy image and entity information for each text in the data
                displacy_image, entities = display_entities(text)

                # Write displacy image, a horizontal line, and entity information to the HTML file
                file.write(displacy_image)
                file.write("\n<hr>\n")
                file.write(str(entities))
                file.write("\n\n")

    def extract_entities_as_df(self, note_list, col_name):
        # Create an empty DataFrame to store the concepts
        df = pd.DataFrame(columns=[col_name])
        # Extract concepts for each note in the provided list
        for note in note_list:
            doc = self.nlp(note)

            # Extract preferred names of concepts and store in a list
            list_of_concepts = [ent.text for ent in doc.ents]

            # Append the concepts for the current note to the DataFrame
            df.loc[len(df.index)] = ', '.join(list_of_concepts)

        return df  # Return the entire DataFrame, not just a column

if __name__ == "__main__":
    def add_col_from_entity(model_name, data_loader):
        # Create an instance of SciSpacyEntityExtractor with the specified model name
        entity_analyzer = SciSpacyEntityExtractor(model_name=model_name)

        # Add a new column to the data_loader with entities extracted using SciSpacy
        data_loader.add_column(entity_analyzer.extract_entities_as_df(data_loader.return_sentences().to_list(),
                                                                     "SciSpacy " + entity_analyzer.model_name),
                               "SciSpacy " + entity_analyzer.model_name)

    def iterate_through_models(list_of_models, data_loader):
        # Iterate through the list of SpaCy models and add corresponding columns to the data_loader
        for model in list_of_models:
            add_col_from_entity(model, data_loader)
