# Cohort-Builder

This is the API layer for DocPlot.

## Running the App

### Install Requirements

```
$ pip install -r requirements.txt
```

### Set up the database

1. Download neo4j 2.2 here
    * http://neo4j.com/download-thanks/?edition=community&flavour=unix&release=2.2.0
2. Extract the neo4j package from the download above
3. Download the DocPlot data zip file here
    * https://drive.google.com/open?id=0B5VudqrtA4nUUTIyMXlBT1lBQVk&authuser=0
4. Extract the _graph.db_ folder from the zip file above
5. Replace the _neo4j-community-2.2.0/data/graph.db_ folder with the DocPlot _graph.db_ folder extracted from the download above
6. Shut down any existing versions of neo4j you have running, and start the 2.2 version 
    * ```neo4j-community-2.2.0/bin/neo4j start ```
7. Change the neo4j username and password (go to localhost:7474 in your web browser and you'll be prompted to change it)
    * Username: neo4j
    * Password: neo

### Install Dependencies

```
$ pip install flask
$ pip install neo4jrestclient
$ pip install graphlab-create
$ pip install pandas
```

### Run the app

```
$ python Cohort\ Builder.py
```

### Sample Request(TBD) 

```
Cohort:
http://127.0.0.1:5001/_api/v1/cohort/

Provider:
http://127.0.0.1:5001/_api/v1/provider/?p_id=4510,14297
```