# Python-FlaskWebsite

## Overview
This project invovles using [Flask](https://flask.palletsprojects.com/en/1.1.x/) to run the website and [psycopg2](https://pypi.org/project/psycopg2/) to connect to a PostgreSQL database.
The data is then interpreted to html through the use of [Jinja](https://jinja.palletsprojects.com/en/2.11.x/templates/).

The website connects to a database that stores data on Steam games and transforms the data to provide insight on purchases.
The data is shown through the use of graphs/charts with templates from [Google charts](https://developers.google.com/chart/interactive/docs/gallery)

Homepage ui

![image](https://user-images.githubusercontent.com/61431892/117088109-857bb300-ad1f-11eb-9110-aaf556f3bb2a.png)


Example query

![steamchart](https://user-images.githubusercontent.com/61431892/117088741-52d2ba00-ad21-11eb-9268-92b6ac75cb9c.png)
