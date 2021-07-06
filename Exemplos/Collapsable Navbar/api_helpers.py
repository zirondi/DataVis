import requests
import json
import os
import pandas as pd

def json_to_df(resp):
    columns = [col['name'] for col in resp.json()['columns']]
    values = resp.json()['rows']
    
    return pd.DataFrame(values, columns=columns)


def executa_sql(token, url_base, query):
  sql = {
          "token":{"token":token}, 
          "sql":{"sql":query}
        }
  resp = requests.post(os.path.join(url_base,'sql_query'), json=sql) 

  return json_to_df(resp)