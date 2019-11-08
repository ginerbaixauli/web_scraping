#!/usr/bin/env python
# coding: utf-8

# Import libraries
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

# Obtain xml text from webpage
web = requests.get('https://en.wikipedia.org/wiki/List_of_cities_proper_by_population').text
soup = BeautifulSoup(web,'xml')
print(soup.prettify())

# Search table and rows in the document
table = soup.find('table', {'class':'sortable wikitable mw-datatable'})
table_rows = table.find_all('tr')

# Save information in a dataset
data = []
for row in table_rows:
    data.append([t.text.strip() for t in row.find_all('td')])

# Obtain column names
columns = []
columns.append([t.text.strip() for t in table_rows[0].find_all('th')])
columns = columns[0]

# Filter useful columns
df = pd.DataFrame(data, columns=columns)
df = df[['City', 'Population', 'Country']]

# Dataset cleaning
df = df.drop(df.index[0])
df['Population'] = df['Population'].str.replace(r'\[.*?\]','')
df['Population'] = df['Population'].str.replace(r',','')
df['Population'] = pd.to_numeric(df['Population'])

# Save dataset as CSV
df.to_csv("dataset.csv")
