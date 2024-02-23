import pandas as pd
from dataloader import DataArranger

class Validator:
    def __init__(self, col_name, gold_label, file_path_to_xlsx_of_data):
        # Initialize the DataArranger for loading data
        self.data_loader = DataArranger(file_path_to_xlsx=file_path_to_xlsx_of_data)
        self.col_name = col_name

        # Load and preprocess data
        self.data = self.data_loader.hydron_dataset[col_name].apply(str).apply(str.lower)
        self.gold_label = self.data_loader.hydron_dataset[gold_label].apply(str.lower)

        # Scores
        # Phrase Level
        self.phrase_level_precision = []
        self.phrase_level_recall = []
        self.phrase_level_f_measure = []

        # Token Level
        self.token_level_precision = []
        self.token_level_recall = []
        self.token_level_f_measure = []

        # Attributes
        self.correctly_returned_tokens = []
        self.tokens_in_output = []
        self.tokens_in_gold_standard = []
        self.correctly_returned_phrases = []
        self.phrases_in_output = []
        self.phrases_in_gold_standard = []

        # Analyze the data
        self.iterate()

    def find_matches(self, index):
        # Extract phrases from the data and ground truth
        output_phrases = [phrase.strip() for phrase in self.data.loc[index].split()]
        gold_label_phrases = [phrase.strip() for phrase in self.gold_label.loc[index].split()]

        # Count the number of phrases in the output and gold standard
        self.phrases_in_output.append(len(output_phrases))
        self.phrases_in_gold_standard.append(len(gold_label_phrases))

        # Extract words from the phrases
        output_words = [word for phrase in output_phrases for word in phrase.split()]
        gold_label_words = [word for phrase in gold_label_phrases for word in phrase.split()]

        # Count the number of tokens in the output and gold standard
        self.tokens_in_output.append(len(output_words))
        self.tokens_in_gold_standard.append(len(gold_label_words))

        # Find common words between output and gold standard
        common_words = set(output_words) & set(gold_label_words)
        self.correctly_returned_tokens.append(len(common_words))

        # Find common phrases between output and gold standard
        common_phrases = [phrase for phrase in output_phrases if phrase in gold_label_phrases]
        self.correctly_returned_phrases.append(len(common_phrases))

    def iterate(self):
        # Iterate through the data to find matches
        for index in range(len(self.gold_label)):
            self.find_matches(index)

        # Calculate precision, recall, f1 score at both phrase and token levels
        for index in range(len(self.gold_label)):
            self.phrase_level_precision.append((self.correctly_returned_phrases[index] / self.phrases_in_output[index]))
            self.phrase_level_recall.append((self.correctly_returned_phrases[index] / self.phrases_in_gold_standard[index]))
            
            # Calculate F1 score for phrase level
            if self.phrase_level_precision[-1] + self.phrase_level_recall[-1] == 0:
                self.phrase_level_f_measure.append(0.0)
            else:
                self.phrase_level_f_measure.append((2 * self.phrase_level_precision[-1] * self.phrase_level_recall[-1]) /
                                                   (self.phrase_level_precision[-1] + self.phrase_level_recall[-1]))
           
            self.token_level_precision.append((self.correctly_returned_tokens[index] / self.tokens_in_output[index]))
            self.token_level_recall.append((self.correctly_returned_tokens[index] / self.tokens_in_gold_standard[index]))
           
            # Calculate F1 score for token level
            if self.token_level_precision[-1] + self.token_level_recall[-1] == 0:
                self.token_level_f_measure.append(0.0)
            else:
                self.token_level_f_measure.append((2 * self.token_level_precision[-1] * self.token_level_recall[-1]) /
                                                  (self.token_level_precision[-1] + self.token_level_recall[-1]))

    def print_debug(self):
        # Print debug information
        print(
            self.correctly_returned_tokens,
            self.tokens_in_output,
            self.tokens_in_gold_standard,
            self.correctly_returned_phrases,
            self.phrases_in_output,
            self.phrases_in_gold_standard
        )

    def add_columns_to_excel(self, new_file_path):
        # Add calculated scores as new columns to the existing Excel file
        df = pd.read_excel(new_file_path)
        df['PLP ' + self.col_name] = pd.DataFrame({'PLP ' + self.col_name: self.phrase_level_precision})
        df['PLR ' + self.col_name] = pd.DataFrame({'PLR ' + self.col_name: self.phrase_level_recall})
        df['Phrase F1 ' + self.col_name] = pd.DataFrame({'Phrase F1 ' + self.col_name: self.phrase_level_f_measure})

        df['TLP ' + self.col_name] = pd.DataFrame({'TLP ' + self.col_name: self.token_level_precision})
        df['TLR ' + self.col_name] = pd.DataFrame({'TLR ' + self.col_name: self.token_level_recall})
        df['Token F1 ' + self.col_name] = pd.DataFrame({'Token F1 ' + self.col_name: self.token_level_f_measure})

        df.to_excel(new_file_path)

    def print_scores(self):
        # Print the calculated scores
        print("Phrase Level Precision:", format(sum(self.phrase_level_precision) / len(self.phrase_level_precision), ".3f"))
        print("Phrase Level Recall:", format(sum(self.phrase_level_recall) / len(self.phrase_level_recall), ".3f"))
        print("Token Level Precision:", format(sum(self.token_level_precision) / len(self.token_level_precision), ".3f"))
        print("Token Level Recall:", format(sum(self.token_level_recall) / len(self.token_level_recall), ".3f"))
        print("Phrase Level F1:", format(sum(self.phrase_level_f_measure) / len(self.phrase_level_f_measure), ".3f"))
        print("Token Level F1:", format(sum(self.token_level_f_measure) / len(self.token_level_f_measure), ".3f"))
