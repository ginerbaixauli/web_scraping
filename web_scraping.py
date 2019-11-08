#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Importamos las librerías
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re


# In[2]:


# Obtenemos el texto en xml de la página web
web = requests.get('https://en.wikipedia.org/wiki/List_of_cities_proper_by_population').text
soup = BeautifulSoup(web,'xml')


# In[3]:


print(soup.prettify())


# In[4]:


# Buscamos la tabla y sus filas en el documento
table = soup.find('table', {'class':'sortable wikitable mw-datatable'})
table_rows = table.find_all('tr')


# In[5]:


# Guardamos la información en un dataset
data = []
for row in table_rows:
    data.append([t.text.strip() for t in row.find_all('td')])


# In[6]:


# Obtenemos los nombres de las columnas
columns = []
columns.append([t.text.strip() for t in table_rows[0].find_all('th')])
columns = columns[0]


# In[7]:


# Filtramos las columnas que nos interesan
df = pd.DataFrame(data, columns=columns)
df = df[['City', 'Population', 'Country']]


# In[8]:


# Limpiamos el dataset
df = df.drop(df.index[0])
df['Population'] = df['Population'].str.replace(r'\[.*?\]','')
df['Population'] = df['Population'].str.replace(r',','')
df['Population'] = pd.to_numeric(df['Population'])


# In[9]:


df.head()


# In[10]:


#Guardamos el dataset en formato csv
df.to_csv("dataset.csv")


# In[ ]:




