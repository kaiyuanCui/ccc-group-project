# API Endpoints Documentation

Base URL: http://127.0.0.1:9090

## Income
**Endpoint:** `/get-income-data/year/{year:[0-9]{4}}`  
**Description:** Retrieves the processed income data for the specified year.

## Crime 
**Endpoint:** `/get-crime-data`  
**Description:** Retrieves cleaned crime data.

## Population 
**Endpoint:** `/get-pop-data`  
**Description:** Retrieves cleaned population data.

## Homeless
**Endpoint:** `/get-homeless-data`
**Description:** Retrieves the preprocessed homeless data.


## Geodata
**Endpoint:** `/get-geodata`  
**Description:** Retrieves raw geodata.

**Parameters:**
  - `limit` (integer): Size of the search, defaults to 999.
  - `from-last` (integer): Makes it start the search from the last `from-last` number of docs.

**Example:**
```
http://127.0.0.1:9090/get-geodata?from-last=true&limit=1
```

## EPA (Filtered)
**Endpoint:** `/get-epa-data`
**Description:** Retrieves real-time data harvested from EPA
**Parameters:**
- **start:** `yyyy-MM-ddTHH:mm:ss` (add `Z` for UTC time)
- **end:** `yyyy-MM-ddTHH:mm:ss` (add `Z` for UTC time)
- **limit:** integer, size of the search, default to 999
- **from-last:** integer, makes it start the search from the last from-last number of docs

**Example:**
http://127.0.0.1:9090/get-epa-data?start=2023-05-12T06:00:00Z&end=2024-05-12T07:00:00Z&from-last=true&limit=1

## BoM 
**Description:** Retrieves real-time data harvested from BoM
**Endpoint:** `/get-bom-data`

**Parameters:**
- **start:** `yyyyMMddHHmmss`
- **end:** `yyyyMMddHHmmss`

**Example:**
http://127.0.0.1:9090/get-bom-data?start=20240516220000&end=20240517220000


## Upload Data
**Description:** Uploads any data to ES, given an index name and the data.

**Endpoint:** `/post-data`
**Request body:**
```json
{
    "index_name": "string",
    "data": {}
}
