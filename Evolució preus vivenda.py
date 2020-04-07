#!/usr/bin/env python
# coding: utf-8

# ## Web scraping

# In[9]:


import bs4 as bs
import urllib
import urllib.request
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io


#retorna un llistat de ciutats i la seva variació de preu segons el html ja llegit per BeatifulSoup que li hem passat. Aquest html està format segons 
# la provincia. Per exemple: HTML = "https://www.trovimap.com/precio-vivienda/barcelona" retornarà un llistat amb les
# ciutats que es troben en aquesta pàgina que son les ciutats de Barcelona i les seves variacions de preus mensual, els últims 3 mesos
# anual i preu euro/ metre quadrat.

def obtenirCiutatsiVariacio(htmlSoup):
    tableProv = soup.find('table', {'class':'table table-condensed precio-medio-table'})

    tbody = tableProv.find('tbody')

    llistaVarCiutats=[]
    for row in tbody.findAll("tr"):
        cells = row.findAll('td')    
        link = cells[0].find('a')
        ciutat = link.find(text=True)
        print (ciutat)
        varMensual = cells[1].find(text=True)
        var3mesos = cells[2].find(text=True)
        varAnual = cells[3].find(text=True)
        eumetre = cells[4].find(text=True)
        element=[ciutat,varMensual,var3mesos,varAnual,eumetre]
        llistaVarCiutats.append(element)
        
        
    return llistaVarCiutats

# In[10]:


HTML = "https://www.trovimap.com/precio-vivienda/barcelona"


# In[11]:


# Amb .read_html() podem obtenir fàcilment la taula que ens mostra la web.

df = pd.read_html(HTML)
df[0].head()


# In[12]:


# Amb BeautifulSoup, podrem obtenir tot el String del codi HTML per si volem obtenir més informació.

df = pd.DataFrame()

historypage = urllib.request.urlopen(HTML)
soup = bs.BeautifulSoup(historypage,'html.parser')
makeitastring = ''.join(map(str, soup))

VarCiutat = obtenirCiutatsiVariacio(soup)

print(VarCiutat[0])

# In[ ]:





# In[ ]:




