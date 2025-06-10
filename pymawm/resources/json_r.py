import pandas
from pandas import json_normalize
from prettyprinter import cpprint

def print_to_table(data):
    df = json_normalize(data)
    delete_list = {'ContextId', 'PK', 'Unique_Identifier', 'Messages'}
    for col in delete_list:
        try:
            df = df.drop(labels=col, axis=1)
        except:
            raise
            continue
    return df


