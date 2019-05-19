the script in src was scheduled to, every 15 min get the availability of every GIRA station around lisbon and store it into a Postgres db for a full month.
This folder has an extract of the data accumulated in that database separated in two files: 
	- db_extract (the factual table in csv and pickle formats) and
	response-state_of_all_GIRA_stations.json that contains a full output of a GET request, to be used as dim table (contains info about each station such as location and description)