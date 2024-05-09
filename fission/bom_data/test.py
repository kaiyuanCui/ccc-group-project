import logging, json, requests, socket
import pandas as pd
def main():
    # api refs: http://www.bom.gov.au/catalogue/data-feeds.shtml
    data=requests.get('http://reg.bom.gov.au/fwo/IDV60901/IDV60901.95936.json').json()
    print(data)
    df = pd.DataFrame.from_dict(data['observations']['data'])
    #print(df.head(15))
    #print(df)

    return df

main()