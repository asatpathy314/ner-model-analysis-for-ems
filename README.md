# ner-model-analysis-for-ems
This repository contains a set of tools for analyzing named entity recognition (NER) for Emergency Medical Services (EMS) data. The tools are designed to extract and analyze entities related to medical concepts from unstructured text data commonly found in EMS transcriptions.

## Tools Overview

### 1. SciSpacy Entity Extractor

The `SciSpacyEntityExtractor` tool utilizes the SciSpacy library for entity extraction using any currently available SciSpacy model. It provides functionalities to analyze and save entities to an HTML file, as well as extract entities from a list of notes and add the results as a new column to a DataFrame.

### 2. MetaMap Entity Extractor

The `MetaMapEntityExtractor` tool integrates with MetaMap, a program developed by the National Library of Medicine (NLM), to extract concepts from clinical text. It includes features to start MetaMap servers, extract concepts to a file, and add extracted concepts as a new column to a DataFrame.

### 3. Data Arranger

The `DataArranger` class is a utility for loading and arranging data from Excel files and then writing back into the data files. It provides methods to return ground truth information, replace abbreviations, return sentences, and add ground truth columns to the DataFrame. For DataArranger to work, the EMS transcription column should be named 'Transcription' and you should name your Ground Truth column as ' NER Ground Truth.' Ensure that your ground truth is in the format CATEGORY, BOOL, NAME; etcetera. 

### 4. Validator

The `Validator` class is responsible for comparing and evaluating the performance of different NLP tools. It calculates precision, recall, and F1 score at both phrase and token levels based on the extracted entities. It uses formulas provided in https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2995677/.

## Getting Started

1. **Configure MetaMap:**
   - If using the `MetaMapEntityExtractor`, make sure to provide the correct paths for MetaMap binaries and servers in the `MetaMapEntityExtractor` constructor.

2. **Start MetaMap Servers:**
   - If utilizing MetaMap, start the part-of-speech tagger and word sense disambiguation servers using the `start_servers` method of `MetaMapEntityExtractor`.

3. **Run the Tools:**
   - Utilize the provided scripts or integrate the tools into your workflow as needed.

## Usage

### 1. Setting up the Data Loader

- Ensure you have a dataset in an Excel file.
- Instantiate the `DataArranger` class in `dataloader.py`:

    ```python
    data_loader = DataArranger(file_path_to_xlsx="your_dataset.xlsx", names=True)
    ```

### 2. Adding Ground Truth Column

- Add a ground truth column to your dataset:

    ```python
    data_loader.add_ground_truth_column(column_name="GroundTruthNames")
    ```

### 3. Adding a New Column

- Add a new column to your dataset using a DataFrame:

    ```python
    # Example DataFrame creation
    df = pd.DataFrame(data={'NewColumnName': ['value1', 'value2', ...]})
    data_loader.add_column(df=df, col_name="NewColumnName")
    ```

### 4. MetaMap Entity Extraction

- Install MetaMap and its dependencies.
- Instantiate the `MetaMapEntityExtractor` class in `concept_extractor_metamap.py`:

    ```python
    metamap_extractor = MetaMapEntityExtractor(base_dir="your_metamap_directory")
    ```

- Start MetaMap servers:

    ```python
    metamap_extractor.start_servers()
    ```

- Extract concepts and save them to a DataFrame:

    ```python
    your_note_list = [...]  # List of notes to extract concepts from
    df_concepts = metamap_extractor.extract_concepts_as_df(note_list=your_note_list, col_name="Concepts")
    df_concepts.to_excel("metamap_concepts_output.xlsx")
    ```

### 5. SciSpacy Entity Extraction

- Instantiate the `SciSpacyEntityExtractor` class in `concept_extractor_scispacy.py`:

    ```python
    scispacy_extractor = SciSpacyEntityExtractor(model_name="en_core_sci_sm")
    ```

- Analyze entities and save them to a DataFrame:

    ```python
    your_note_list = [...]  # List of notes to extract entities from
    df_entities = scispacy_extractor.extract_entities_as_df(note_list=your_note_list, col_name="Entities")
    df_entities.to_excel("scispacy_entities_output.xlsx")
    ```

### 6. Validator for NER Ground Truth Evaluation

- Instantiate the `Validator` class in `validator.py` for evaluating NER ground truth against model predictions:

    ```python
    checker = Validator(col_name="your_column_name", gold_label="your_ground_truth_column", file_path_to_xlsx_of_data="your_dataset.xlsx")
    ```

    - `col_name`: The column containing model predictions.
    - `gold_label`: The column containing the ground truth.
    - `file_path_to_xlsx_of_data`: Path to the dataset Excel file.

- Print debug information (optional):

    ```python
    checker.print_debug()
    ```

- Print and add calculated scores as new columns to the existing Excel file:

    ```python
    checker.print_scores()
    checker.add_columns_to_excel(new_file_path="output_with_scores.xlsx")
    ```

---

Make sure to replace placeholders like `"your_column_name"`, `"your_ground_truth_column"`, `"your_dataset.xlsx"`, etc., with the actual values specific to your project. Adjust the example usage accordingly.