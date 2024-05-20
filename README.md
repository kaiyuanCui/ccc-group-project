# Homelessness Analysis

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Data Sources](#data-sources)
- [Cloud Conncection](#cloud-connection)
- [Results](#results)

## Introduction
This project aims to integrate, analyze and visualize data from different data sources - SUDO platform, Bureau of Meteorology (BoM) data and Environmental Protection Agency (EPA) data - to research potential relationship between environmental, income, demographic factors and homelessness across Local Government Areas (LGAs). Using Melbourne Research Cloud, Kubernetes, Docker, Fission and ElasticSearch, we developed a cloud-based solution that efficiently pulls, stores and analyses data to draw meaningful conclusions and insights.

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
example: 'http://reg.bom.gov.au/fwo/IDV60901/IDV60901.95936.json' \
Environmental Protection Agency (EPA) data: https://gateway.api.epa.vic.gov.au/environmentMonitoring/v1/sites/parameters?environmentalSegment=air \

## Cloud Connection
First Connect Kubernetes Cluster:
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