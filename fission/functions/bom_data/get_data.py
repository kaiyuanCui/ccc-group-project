import json, requests

import pandas as pd
import requests
from flask import current_app, request
from pathlib import Path
from io import StringIO

INDEX_NAME = 'bom'
IS_LOCAL = False
UPLOAD = True
#BASE_PATH = Path(__file__).parent
#STATIONS_LIST = (BASE_PATH /'stations_list.csv').resolve()

# TODO: potentially save these to es and read from there
STATIONS_CSV = '''
Unnamed: 0,Site name,Lat,Lon,STA,WMO
55,PERTH AIRPORT,-31.9275,115.9764,WA,94610
57,PEARCE RAAF,-31.6669,116.0189,WA,94612
58,INNER DOLPHIN PYLON,-31.9889,115.8311,WA,95620
59,GOSNELLS CITY,-32.0481,115.9844,WA,95604
60,KARNET,-32.4389,116.0789,WA,95614
62,JANDAKOT AERO,-32.1011,115.8794,WA,94609
64,ROTTNEST ISLAND,-32.0069,115.5022,WA,94602
65,OCEAN REEF,-31.7594,115.7278,WA,94607
66,SWANBOURNE,-31.956,115.7619,WA,94614
67,PERTH METRO,-31.9192,115.8728,WA,94608
68,BICKLEY,-32.0072,116.1369,WA,95610
69,ARMAMENT JETTY,-32.1758,115.6808,WA,99254
70,COLPOYS POINT,-32.2272,115.6994,WA,99255
71,GARDEN ISLAND HSF,-32.2433,115.6839,WA,95607
72,HILLARYS BOAT HARBOUR NTC AWS,-31.8256,115.7386,WA,95605
75,MILLENDON (SWAN VALLEY),-31.8112,116.0227,WA,94795
96,MANDURAH,-32.5219,115.7119,WA,94605
267,ADELAIDE (WEST TERRACE / NGAYIRDAPIRA),-34.9257,138.5832,SA,94648
268,PARAFIELD AIRPORT,-34.7977,138.6281,SA,95677
269,ADELAIDE AIRPORT,-34.9524,138.5196,SA,94672
270,OUTER HARBOUR (BLACK POLE),-34.7343,138.4653,SA,95675
271,EDINBURGH RAAF,-34.7111,138.6223,SA,95676
273,ROSEWORTHY AWS,-34.5106,138.6763,SA,95671
277,NURIOOTPA PIRSA,-34.4761,139.0056,SA,94681
278,MOUNT BARKER,-35.0732,138.8466,SA,94806
280,VICTOR HARBOR (ENCOUNTER BAY),-35.5544,138.5997,SA,95811
281,MOUNT LOFTY,-34.9784,138.7088,SA,95678
282,PARAWA (SECOND VALLEY FOREST AWS),-35.5695,138.2864,SA,94811
283,MOUNT CRAWFORD AWS,-34.7253,138.9278,SA,94678
284,NOARLUNGA,-35.1586,138.5057,SA,94808
285,SELLICKS HILL (MOUNT TERRIBLE RADAR),-35.3294,138.5019,SA,95679
286,KUITPO FOREST RESERVE,-35.1712,138.6783,SA,94683
287,HINDMARSH ISLAND AWS,-35.5194,138.8177,SA,94677
292,MURRAY BRIDGE,-35.1234,139.2592,SA,95812
293,STRATHALBYN RACECOURSE,-35.2836,138.8934,SA,94814
294,MURRAY BRIDGE (PALLAMANA AERODROME),-35.065,139.2273,SA,95818
409,AMBERLEY AMO,-27.6297,152.7111,QLD,94568
410,CAPE MORETON LIGHTHOUSE,-27.0314,153.4661,QLD,94594
411,DOUBLE ISLAND POINT LIGHTHOUSE,-25.9319,153.1906,QLD,94584
412,UNIVERSITY OF QUEENSLAND GATTON,-27.5436,152.3375,QLD,94562
413,GYMPIE,-26.1831,152.6414,QLD,94566
415,POINT LOOKOUT,-27.4361,153.5456,QLD,94593
416,ARCHERFIELD AIRPORT,-27.5716,153.0071,QLD,94575
417,BEERBURRUM FOREST STATION,-26.9586,152.9619,QLD,95566
420,COOLANGATTA,-28.1681,153.5053,QLD,94592
421,GOLD COAST SEAWAY,-27.939,153.4283,QLD,94580
422,BRISBANE AERO,-27.3917,153.1292,QLD,94578
423,LOGAN CITY WATER TREATMENT PLANT,-27.6841,153.1981,QLD,95581
424,RAINBOW BEACH,-25.9007,153.0891,QLD,94564
425,SUNSHINE COAST AIRPORT,-26.599,153.0912,QLD,94569
426,TEWANTIN RSL PARK,-26.3911,153.0403,QLD,94570
427,BRISBANE,-27.4808,153.0389,QLD,94576
428,KINGAROY AIRPORT,-26.5737,151.8398,QLD,94549
429,BANANA BANK NORTH BEACON,-27.5327,153.3333,QLD,94591
430,INNER RECIPROCAL MARKER,-27.2633,153.2419,QLD,94590
431,SPITFIRE CHANNEL BEACON,-27.0481,153.2664,QLD,94581
432,REDCLIFFE,-27.2169,153.0922,QLD,95591
435,BEAUDESERT DRUMLEY STREET,-27.9707,152.9898,QLD,95575
436,NAMBOUR DAFF - HILLSIDE,-26.6442,152.9383,QLD,95572
440,OAKEY AERO,-27.4034,151.7413,QLD,94552
442,WARWICK,-28.2061,152.1003,QLD,94555
443,TOOWOOMBA AIRPORT,-27.5425,151.9134,QLD,95551
550,NEWCASTLE NOBBYS SIGNAL STATION AWS,-32.9184,151.7985,NSW,94774
551,WILLIAMTOWN RAAF,-32.7939,151.8364,NSW,94776
558,NORAH HEAD AWS,-33.2814,151.5766,NSW,95770
559,MANGROVE MOUNTAIN AWS,-33.2894,151.2107,NSW,95774
561,COORANBONG (LAKE MACQUARIE AWS),-33.0887,151.4636,NSW,95767
562,GOSFORD AWS,-33.4351,151.3614,NSW,94782
570,KATOOMBA (FARNELLS RD),-33.7139,150.2953,NSW,94744
574,MOUNT BOYCE AWS,-33.6185,150.2741,NSW,94743
586,FORT DENISON,-33.8551,151.2254,NSW,94769
587,SYDNEY AIRPORT AMO,-33.9465,151.1731,NSW,94767
588,KURNELL AWS,-34.0039,151.2111,NSW,95756
589,LITTLE BAY (THE COAST GOLF CLUB),-33.9829,151.2502,NSW,94780
590,TERREY HILLS AWS,-33.6908,151.2253,NSW,94759
591,PARRAMATTA NORTH (MASONS DRIVE),-33.7917,151.0181,NSW,94764
592,BANKSTOWN AIRPORT AWS,-33.9176,150.9837,NSW,94765
593,HOLSWORTHY AERODROME AWS,-33.9925,150.9489,NSW,95761
596,CANTERBURY RACECOURSE AWS,-33.9057,151.1134,NSW,94766
597,SYDNEY HARBOUR (WEDDING CAKE WEST),-33.8405,151.2643,NSW,95766
598,MANLY (NORTH HEAD),-33.8152,151.2986,NSW,95768
599,WATTAMOLLA AWS,-34.1407,151.1185,NSW,95752
601,SYDNEY OLYMPIC PARK AWS (ARCHERY CENTRE),-33.8338,151.0718,NSW,95765
602,SYDNEY (OBSERVATORY HILL),-33.8593,151.2048,NSW,94768
604,PROSPECT RESERVOIR,-33.8193,150.9127,NSW,94736
605,RICHMOND RAAF,-33.6004,150.7761,NSW,95753
606,BADGERYS CREEK AWS,-33.8969,150.7281,NSW,94752
607,PENRITH LAKES AWS,-33.7195,150.6783,NSW,94763
608,HORSLEY PARK EQUESTRIAN CENTRE AWS,-33.851,150.8567,NSW,94760
611,CAMDEN AIRPORT AWS,-34.039,150.689,NSW,94755
613,BELLAMBI AWS,-34.3691,150.9291,NSW,94749
619,CAMPBELLTOWN (MOUNT ANNAN),-34.0615,150.7735,NSW,94757
624,HOLSWORTHY DEFENCE AWS,-34.081,150.9009,NSW,95684
732,ESSENDON AIRPORT,-37.7276,144.9066,VIC,95866
733,VIEWBANK,-37.7408,145.0972,VIC,95874
734,MOORABBIN AIRPORT,-37.98,145.0962,VIC,94870
735,SCORESBY RESEARCH INSTITUTE,-37.871,145.2561,VIC,95867
737,ST KILDA HARBOUR - RMYS,-37.864,144.9639,VIC,95864
738,FERNY CREEK,-37.8748,145.3497,VIC,94872
739,MELBOURNE AIRPORT,-37.6654,144.8322,VIC,94866
740,MELBOURNE (OLYMPIC PARK),-37.8255,144.9816,VIC,95936
741,SOUTH CHANNEL ISLAND,-38.3065,144.8016,VIC,94853
742,BUNDOORA (LATROBE UNIVERSITY),-37.7163,145.0453,VIC,95873
743,CERBERUS,-38.3646,145.1785,VIC,94898
744,FRANKSTON BEACH,-38.148,145.1152,VIC,94871
745,RHYLL,-38.4612,145.3101,VIC,94892
746,FAWKNER BEACON,-37.9483,144.9269,VIC,95872
747,COLDSTREAM,-37.7239,145.4092,VIC,94864
748,FRANKSTON (BALLAM PARK),-38.1517,145.1615,VIC,94876
749,LAVERTON RAAF,-37.8565,144.7565,VIC,94865
751,AVALON AIRPORT,-38.0288,144.4783,VIC,94854
752,POINT WILSON,-38.0958,144.5361,VIC,94847
753,SHE OAKS,-37.9075,144.1303,VIC,94863
755,BREAKWATER (GEELONG RACECOURSE),-38.1737,144.3765,VIC,94857
756,POINT COOK RAAF,-37.9273,144.7566,VIC,95941
797,ORFORD (AUBIN COURT),-42.5519,147.8753,TAS,95984
802,MARIA ISLAND (POINT LESUEUR),-42.6621,148.0179,TAS,95988
807,HOBART AIRPORT WEST,-42.8339,147.5033,TAS,94975
808,CAPE BRUNY LIGHTHOUSE,-43.4892,147.1453,TAS,94967
809,DOVER,-43.333,146.998,TAS,94961
810,HOBART (ELLERSLIE ROAD),-42.8897,147.3278,TAS,94970
812,KUNANYI (MOUNT WELLINGTON PINNACLE),-42.895,147.2358,TAS,95979
813,TASMAN ISLAND,-43.2397,148.0025,TAS,95986
817,CAPE BRUNY (CAPE BRUNY),-43.4886,147.1444,TAS,95967
818,CAMPANIA (KINCORA),-42.6867,147.4258,TAS,95972
819,GROVE (RESEARCH STATION),-42.9844,147.0756,TAS,95977
820,HOBART AIRPORT,-42.8333,147.5119,TAS,94619
821,DUNALLEY (STROUD POINT),-42.9017,147.7894,TAS,94951
822,DENNES POINT,-43.0639,147.3567,TAS,94988
825,BUSHY PARK (BUSHY PARK ESTATES),-42.7097,146.8983,TAS,94964
840,REDLAND (ALEXANDRA HILLS),-27.5433,153.2394,QLD,94561
841,CANUNGRA (DEFENCE),-28.0437,153.1871,QLD,94418
842,GREENBANK (DEFENCE),-27.6932,152.9935,QLD,94419
843,TIN CAN BAY (DEFENCE),-25.9351,152.9647,QLD,94420
864,NORTH WEST 10 BEACON,-27.0,153.242,QLD,99496
865,HOPE BANKS BEACON,-27.4344,153.2904,QLD,99497
'''

# Uplaod to Elastic Search
def upload_es(index_name:str, data:pd.DataFrame) -> bool:
    # request settings:
    url =''
    if IS_LOCAL:
        url = 'https://localhost:9200'
    else:
        url = 'https://elasticsearch-master.elastic.svc.cluster.local:9200'


    headers = {'Content-Type': 'application/json'}
    auth = ('elastic', 'elastic')
    requests.packages.urllib3.disable_warnings()
    verify_ssl = False
    index_url = url + '/' + index_name + '/_bulk'

    actions = []
    for index, row in data.iterrows():
        doc_id = row['name'] + row['local_date_time_full'] # assume unique
        # print(doc_id)
        # print("________________")
        # doc_id = doc_id[:20]
        
        payload = row.to_dict()

        for key, value in payload.items():
            if pd.isna(value):
                payload[key] = None
        action = {'index': {'_id': doc_id}}
        actions.append(json.dumps(action))
        actions.append(json.dumps(payload))

    try:
        response = requests.post(index_url, data='\n'.join(actions) + '\n', headers=headers, auth=auth, verify=verify_ssl)
        if IS_LOCAL:
            print(f'Status Code: {response.status_code}')
            print(response.json())
        else:
            current_app.logger.info(f'Status Code: {response.status_code}')
            current_app.logger.info(response.json())
    except requests.RequestException as error:
        print(f'Error: {error}')
        current_app.logger.info(f'Error: {error}')
        return False

    return True

# get latest data from BOM, return as pandas dataframe
def get_latest_data() -> pd.DataFrame:

    stations_info = pd.read_csv(StringIO(STATIONS_CSV))
    df = pd.DataFrame()
    ok_stations = pd.DataFrame(columns=stations_info.columns)
    print(stations_info.head)

    for index, station in stations_info.iterrows():
       # print(station)
        state = station['STA'][0] # first letter in state
        station_wmo = station['WMO']
        
        # assume all are 60901
        url = f'http://reg.bom.gov.au/fwo/ID{state}60901/ID{state}60901.{station_wmo}.json' # example: 'http://reg.bom.gov.au/fwo/IDV60901/IDV60901.95936.json'
        # api refs: http://www.bom.gov.au/catalogue/data-feeds.shtml


        try:
            if IS_LOCAL:
                print(url)
            else:
                current_app.logger.info(url)
            response = requests.get(url)
            if IS_LOCAL:
                print(response)
                print("STATUS CODE:")
                print(response.status_code)
            else:
                current_app.logger.info(response)
            data=response.json()
            
            
            new_df = pd.DataFrame.from_dict(data['observations']['data'])
            df = pd.concat([df, new_df])

            # save the stations that have data to new csv
            ok_stations = pd.concat([
                ok_stations, 
                pd.DataFrame([station])]
           )
            

        except requests.RequestException as error:
            if IS_LOCAL:
                print(f'Error: {error}')
                print(station)
                file1 = open("log.txt", "a")  # append mode
                file1.write(f'Error: {error}\n')
                file1.write(f'Station: {station}\n\n\n')
                file1.close()
            else:
                current_app.logger.info(f'Error: {error}')
    # ok_stations.to_csv('successes.csv', index=False)
    return df
    #print(df.head(15))
    #print(df)


   

def main():
    if IS_LOCAL:
        file1 = open("log.txt", "w")
        L = ["Error LOG"]
        file1.writelines(L)
        file1.close()

    # print("Getting new data")
    data = get_latest_data()
    # print(data)
    if UPLOAD:
        status = upload_es(INDEX_NAME, data)
        if status:
            print("UPLOAD SUCCESS")
            if not IS_LOCAL:
                current_app.logger.info("UPLOAD SUCCESS")

            return "UPLOAD SUCCESS"
        else:
            print("FAILED")
            if not IS_LOCAL:
                current_app.logger.info("UPLOAD FAILED")

            return "UPLOAD FAILED"