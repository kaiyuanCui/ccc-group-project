import json
from elasticsearch8 import Elasticsearch, helpers
import pandas as pd

client = Elasticsearch(
    'https://elasticsearch-master.elastic.svc.cluster.local:9200',
    verify_certs=False,
    ssl_show_warn=False,
    basic_auth=('elastic', 'elastic')
)

def fetch_data_from_es(index_name, query):
    try:
        print("Fetching data from Elasticsearch...")
        response = helpers.scan(client, index=index_name, query=query)
        docs = list(response)
        
        data = [doc['_source'] for doc in docs]
        df = pd.DataFrame(data)
        print("Data fetched successfully.")
        return df
    
    except Exception as e:
        print(f"Error fetching data: {e}")
        return pd.DataFrame() 

def clean_homeless_data(homeless):
    print("Cleaning data...")
    homeless = homeless.fillna(0)
    transformed_data = []

    for column in homeless.columns:
        if column not in [' fin_yr', ' lga_name', ' lga_code']:
            parts = column.split('_')
            if 'homeless' in column:
                type = 'homeless'
            elif 'at_risk' in column:
                type = 'at_risk'
            elif 'ns' in column:
                type = 'not_state'

            if 'm' in parts:
                gender = 'Male'
            elif 'f' in parts:
                gender = 'Female'
            
            if '0_9' in column:
                age_group = '0-9'
            elif '10_19' in column:
                age_group = '10-19'
            elif '20_29' in column:
                age_group = '20-29'
            elif '30_39' in column:
                age_group = '30-39'
            elif '40_49' in column:
                age_group = '40-49'
            elif '50_59' in column:
                age_group = '50-59'
            elif '60_plus' in column:
                age_group = '60+'
            elif 'np' in column:
                age_group = 'not_provide'
            for index, value in homeless[column].items():
                row_data = {
                    'year': homeless[' fin_yr'][index],
                    'lga_name': homeless[' lga_name'][index],
                    'lga_code': homeless[' lga_code'][index],
                    'age_group': age_group,
                    'gender': gender,
                    'homeless_type': type,
                    'count': int(value)
                }
                transformed_data.append(row_data)

    transformed_df = pd.DataFrame(transformed_data)
    type_group_sum = transformed_df.groupby(['year', 'lga_name', 'lga_code', 'homeless_type'])['count'].sum().reset_index()
    type_group_sum.columns = ['year', 'lga_name', 'lga_code', 'homeless_type', 'total_count']
    pivot_homeless_df = type_group_sum.pivot_table(index=['year', 'lga_name', 'lga_code'], columns='homeless_type', values='total_count', aggfunc='first', fill_value=0)
    pivot_homeless_df.reset_index(inplace=True)
    pivot_homeless_df['total'] = pivot_homeless_df[['at_risk', 'homeless', 'not_state']].sum(axis=1)

    return pivot_homeless_df



def main():
   
    query = {
        "query": {
            "match_all": {}
        }
    }
    raw_data = fetch_data_from_es('homeless', query)
    if raw_data.empty:
     
        return

    clean_data = clean_homeless_data(raw_data)
    
    
  
    return clean_data.to_json(orient='records')

if __name__ == '__main__':
    main()
