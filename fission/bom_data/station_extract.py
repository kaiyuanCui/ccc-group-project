import pandas as pd
import requests

def extract_station_list():
    url = 'https://reg.bom.gov.au/climate/data/lists_by_element/stations.txt'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.content.decode('utf-8')
    else:
        raise Exception("Data Download Fail, Status Code:" + str(response.status_code))

    lines = data.splitlines()[2:]
    data_rows = []
    for line in lines:
        if line.strip() and not line.startswith('-------'):
            # extract each column data 
            site = line[0:7].strip()
            dist = line[7:13].strip()
            site_name = line[13:57].strip()
            start = line[57:64].strip()
            end = line[64:71].strip()
            lat = line[71:80].strip()
            lon = line[80:89].strip()
            source = line[89:104].strip()
            sta = line[104:108].strip()
            height = line[108:120].strip()
            bar_ht = line[120:129].strip()
            wmo = line[129:135].strip()

            # Add data into column list
            data_rows.append([site, dist, site_name, start, end, lat, lon, source, sta, height, bar_ht, wmo])

    # Create Dataframe
    columns = ["Site", "Dist", "Site name", "Start", "End", "Lat", "Lon", "Source", "STA", "Height (m)", "Bar_ht", "WMO"]
    df = pd.DataFrame(data_rows, columns=columns)

    column_list = ['Site name', 'Lat', 'Lon', 'STA', 'WMO']

    filtered_df = df[df['WMO'].notna()].reset_index(drop=True)
    filtered_df = filtered_df[filtered_df['WMO'].astype(str).str.match(r'^\d{5}$')].reset_index(drop=True)
    filtered_df = filtered_df[~filtered_df['End'].astype(str).str.match(r'^\d{4}$')].reset_index(drop=True)
    final_station_list = filtered_df[column_list]
    return final_station_list