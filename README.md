# Homelessness Analysis

## Team Members
Team 77: \
Name: Hanchun Pan Student ID: 1266219, Email: hanchunp@student.unimelb.edu.au \
Name: Kaiyuan Cui Student ID: 1266180 , Email: kaicui@student.unimelb.edu.au \
Name: Runyu Yang Student ID: 1118665, Email: runyuy@student.unimelb.edu.au \
Name: Yaotian Wang  Student ID: 1503936, Email: yaotwang@student.unimelb.edu.au \
Name: Zhenghan Zhang Student ID: 1136448, Email: zhenghanz1@student.unimelb.edu.au 
## Table of Contents

- [Introduction](#introduction)
- [Repository Structure](#repository-structure)
- [Installation](#installation)
- [Data Sources](#data-sources)
- [Cloud Conncection](#cloud-connection)
- [Results](#results)
- [Links](#links)

## Introduction
This project aims to integrate, analyze and visualize data from different data sources - SUDO platform, Bureau of Meteorology (BoM) data and Environmental Protection Agency (EPA) data - to research potential relationship between environmental, income, demographic factors and homelessness across Local Government Areas (LGAs). Using Melbourne Research Cloud, Kubernetes, Docker, Fission and ElasticSearch, we developed a cloud-based solution that efficiently pulls, stores and analyses data to draw meaningful conclusions and insights.

## Repository Structure
`backend`: All files in backend folder are used for Restful API:
`data_upload.py`: contains functions upload original sudo data to elasticsearch by fission post API.\
`station_extract.py`: contains functions upload BoM Station list to elasticsearch by fission post API.\
Under fission folder and functions folder in fission includes all packages build in fission:\
`bom_data`: Catch BoM site information through fission by time trigger and store it in elasticsearch.\
`epa`: Catch EPA site information through fission by time trigger and store it in elasticsearch.\
`api`: Include all API functions\
`tests`: Include elasticsearch connection test
`log.txt`: This file contains all log messages. \
`update_api.sh`: Used for updating API Package on Fission. \
`update_bom.sh`: Used for updating `api` and `bom` Package on Fission.

`database`: Include Elastic search mappings of BoM and EPA.

`frontend`: Include `front_end.ipynb` for data analysis and visualization.

`test`: Include all functions used to test restful api either get and post data API.

`.gitignore`: Ignore files which extension include in this file.

`requirements.txt`: include all package need to run front end.



## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/kaiyuanCui/ccc-group-project.git
    cd your-repo-name
    ```
    Replace your-repo-name with your local repository path

2. Create a virtual environment and activate it:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Data Sources
SUDO Platform: https://sudo.eresearch.unimelb.edu.au/ \
Bureau of Meteorology (BoM) Station list: https://reg.bom.gov.au/climate/data/lists_by_element/stations.txt \
Bureau of Meteorology (BoM) Real Time Data: http://reg.bom.gov.au/fwo/ID{state}60901/ID{state}60901.{station_wmo}.json \
Example: 'http://reg.bom.gov.au/fwo/IDV60901/IDV60901.95936.json' \
Environmental Protection Agency (EPA) data: https://gateway.api.epa.vic.gov.au/environmentMonitoring/v1/sites/parameters?environmentalSegment=air

## Cloud Connection
First Connect Melbourne VPN:
Then, Connect Melbourne Research Cloud(MRC):
1. Source the OpenStack RC file in local terminal:
    ```sh
    source ./<your project name>-openrc.s
    ```
    Replace `your project name` with OpenStack RC file name

2. Accessing the Kubernetes Cluster
    ```sh
    chmod 600 <path-to-private-key> (e.g. ~/Downloads/mykeypair.pem)
    ssh -i <path-to-private-key> (e.g. ~/Downloads/mykeypair.pem) -L 6443:$(openstack coe cluster show elastic -f json | jq -r '.master_addresses[]'):6443 ubuntu@$(openstack server show bastion -c addresses -f json | jq -r '.addresses["qh2-uom-internal"][]')
    ```
    Replace `path-to-private-key` with your key pem file path

Next, port forward from the Fission router in a different shell:
1. Port Forward Command:
    ```sh
    kubectl port-forward service/router -n fission 9090:80
    ```

## Result 
The project has revealed several key insights, including the correlation between environmental, income, demographic factors, crime and homelessness. For detailed findings, refer to the senario section in `front_end` jupyter notebook under front-end folder.

## Links
### Restful API
Australia homeless data by LGA: 'http://localhost:9090/get-homeless-data' \
Australia Geometry Data by LGA: 'http://localhost:9090/get-geodata?from-last={index}&limit={limit}' \
Example: 'http://localhost:9090/get-geodata?from-last=100&limit=100'\
Victoria Crime Data by LGA: 'http://localhost:9090/get-crime-data' \
Australia Income and Homeless Data by LGA: 'http://localhost:9090/get-income-data/year/<year_you_want>' \
Example: 'http://localhost:9090/get-income-data/year/2016'\
Australia Population Data by LGA: 'http://localhost:9090/get-pop-data' \
BoM Data by Station: 'http://127.0.0.1:9090/get-bom-data?start={start_time}&end={end_time}&from-last={index}&limit={limit}\
Example: "http://127.0.0.1:9090/get-epa-data?start=2023-05-12T06:00:00Z&end=2024-05-12T07:00:00Z&from-last=true&limit=1"\
Victoria EPA Data By Station: "http://127.0.0.1:9090/get-epa-data?start={start_time}&end={end_time}"\
Example: 'http://127.0.0.1:9090/get-bom-data?start=20240516220000&end=20240517220000' \
Local Upload API: 'http://127.0.0.1:9090/post-data'

### Youtube Video Link
Youtube Link: https://youtu.be/Qn8h7B63aP8