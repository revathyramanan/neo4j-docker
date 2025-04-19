from neo4j_connection import Neo4jConnection
from dotenv import load_dotenv
import os

load_dotenv('../.env')

# Credentials to establish connect to neo4j
URI = 'bolt://localhost:7687'
USER = os.getenv("NEO4J_USER_NAME")
PASSWORD = os.getenv("NEO4J_PASSWD")
AUTH = (os.getenv("NEO4J_USER_NAME"), os.getenv("NEO4J_PASSWD"))

# Instantiate Neo4j connection
neo4j_obj = Neo4jConnection(uri=URI, 
                    user=USER,
                    pwd=PASSWORD)

print(neo4j_obj)

# Query all the nodes from the graph
def convert_to_json(result):
    data_dict = {}
    for item in result:
        curr_dict = dict(item[0])
        item_id = curr_dict['itemID']
        data_dict[item_id] = curr_dict
    return data_dict
    
# 1. Get all the subsitutes for spinach
query_str = """MATCH (n:Ingredient {name:$name})-[r]-(subs:Ingredient) return properties(subs)"""
parameters = {'name':'spinach'}
# 2. Execute the query
response = neo4j_obj.query(query_str, parameters)

# 3. Convert to json for processing
json_res = convert_to_json(response)
for itemID in json_res:
    print(itemID)
    print(json_res[itemID]['name'])
    print("\n")
