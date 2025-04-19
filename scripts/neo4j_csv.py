import pandas as pd
import os
import hashlib
import csv

"""
This file creates intermediate csv files to batch load data into neo4j
"""

BASE_DIR = '../data'
ingredients_path = os.path.join(BASE_DIR, 'ingredients.csv')
substitutions_path = os.path.join(BASE_DIR, 'substitutes.csv')

def create_uuid_from_string(string):
    hex_string = int(hashlib.sha1(string.encode("utf-8")).hexdigest(), 16) % (10 ** 10)
    return str(hex_string)


def write_to_csv(data, filepaths):
    """
    filepaths: a list of paths in case we want to save in two locations
    """
    # writing to a csv file
    csv_data = data

    for filepath in filepaths:
        csv_data_file = open(filepath, 'w')
        # create the csv writer object
        csv_writer = csv.writer(csv_data_file)

        # Counter variable used for writing
        # headers to the CSV file
        count = 0
        for element in csv_data:
            if count == 0:
                # Writing headers of CSV file
                header = element.keys()
                csv_writer.writerow(header)
                count += 1
            # Writing data of CSV file
            csv_writer.writerow(element.values())
        csv_data_file.close()
        print("File saved at:", filepath)


# nodes: which are ingredients
def process_ingredient_nodes(filepath):
    # Read the file
    df = pd.read_csv(filepath)
    data_dict = []
    for i in range(0,len(df)):
        # Create unique ID. Using ingredient names
        ing_name = df['ingredients'][i]
        ing_id = create_uuid_from_string(ing_name.lower())
        ing_link = df['USFDA'][i]
        category = df['category'][i]
        # Create a dict with all properties
        data_dict.append({'id': ing_id, 
                          'name': ing_name,
                          'category': category,
                          'ing_info': ing_link})

    # Save the dicts as csv
    write_to_csv(data_dict, ['../neo4j_raw_data/nodes/ingredient_nodes.csv'])


# relationships: which are subsitution pairs
def process_subsitution_pairs(filepath):
    # Read the file
    df = pd.read_csv(filepath)
    data_dict = []
    for i in range(0,len(df)):
        # we want to save source_node_id and target_node_id.
        # since the pairs are based on the ingredient names, use UUID
        src_id = create_uuid_from_string(df['ing1'][i])
        target_id = create_uuid_from_string(df['ing2'][i])
        src_link = df['src'][i]
        data_dict.append({'src_id': src_id, 'target_id':target_id, 'source':src_link, 'some_prop':'some value'})
    
    # write to file
    write_to_csv(data_dict, ['../neo4j_raw_data/relationships/pairs.csv'])

process_ingredient_nodes(ingredients_path)
process_subsitution_pairs(substitutions_path)